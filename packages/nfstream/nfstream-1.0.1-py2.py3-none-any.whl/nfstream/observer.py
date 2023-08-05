import sys
from cffi import FFI
from collections import namedtuple
from enum import Enum, IntEnum
from time import time, sleep
from select import select
from threading import Lock
from socket import ntohs, ntohl
from .observer_cc import cc
import os.path
TICK_RESOLUTION = 1000

PcapInterface = namedtuple('PcapInterface', ['name', 'internal_name', 'description', 'isloop', 'isup', 'isrunning'])
PcapStats = namedtuple('PcapStats', ['ps_recv', 'ps_drop', 'ps_ifdrop'])
PcapPacket = namedtuple('PcapPacket', ['timestamp', 'capture_length', 'length', 'raw'])
PcapDev = namedtuple('PcapDev', ['dlt', 'nonblock', 'snaplen', 'version', 'pcap'])


PacketInformation = namedtuple('PacketInformation', ['timestamp', 'capture_length', 'length', 'hash', 'ip_src_int',
                                                     'ip_dst_int', 'src_port', 'dst_port', 'ip_protocol', 'vlan_id',
                                                     'version', 'raw'])


class PcapException(Exception):
    pass


def nfstream_hash(ip_src, ip_dst, sport, dport, vlan_id, proto):
    if ip_src < ip_dst:
        return ip_src, ip_dst, sport, dport, vlan_id, proto
    else:
        return ip_dst, ip_src, dport, sport, vlan_id, proto


class Dlt(Enum):
    DLT_NULL = 0
    DLT_EN10MB = 1
    DLT_EN3MB = 2
    DLT_AX25 = 3
    DLT_PRONET = 4
    DLT_CHAOS = 5
    DLT_IEEE802 = 6
    DLT_ARCNET = 7
    DLT_SLIP = 8
    DLT_PPP = 9
    DLT_FDDI = 10
    DLT_PPP_SERIAL = 50
    DLT_RAW = 12
    DLT_C_HDLC = 104
    DLT_LINUX_SLL = 113
    DLT_IEEE802_11_RADIO = 127
    DLT_UNSUPPORTED = 12


class PcapDirection(IntEnum):
    InOut = 0
    In = 1
    Out = 2


class PcapTstampType(IntEnum):
    Host = 0
    HostLowPrec = 1
    HostHighPrec = 2
    Adapter = 3
    AdapterUnsync = 4


class PcapTstampPrecision(IntEnum):
    Micro = 0
    Nano = 1


class PcapWarning(IntEnum):
    Generic = 1
    PromiscNotSupported = 2
    TstampTypeNotSupported = 3


def fcf_type(fc):
    return (fc >> 2) & 0x3


def fcf_subtype(fc):
    return (fc >> 4) & 0xF


def fcf_to_ds(fc):
    return fc & 0x0100


def fcf_from_ds(fc):
    return fc & 0x0200


class _PcapFfi(object):
    '''
    This class represents the low-level interface to the libpcap library.
    It encapsulates all the cffi calls and C/Python conversions, as well
    as translation of errors and error codes to PcapExceptions.  It is
    intended to be used as a singleton class through the PcapDumper
    and PcapLiveDevice classes, below.
    '''
    _instance = None
    __slots__ = ['_ffi', '_libpcap', '_interfaces', '_windoze']

    def __init__(self):
        '''
        Assumption: this class is instantiated once in the main thread before
        any other threads have a chance to try instantiating it.
        '''
        if _PcapFfi._instance:
            raise Exception("Can't initialize this class more than once!")

        _PcapFfi._instance = self
        self._windoze = False
        self._ffi = FFI()
        self._ffi.cdef(cc, override=True)
        if sys.platform == 'darwin':
            libname = 'libpcap.dylib'
        elif sys.platform == 'win32':
            libname = 'wpcap.dll'  # winpcap
            self._windoze = True
        else:
            # if not macOS (darwin) or windows, assume we're on
            # some unix-based system and try for libpcap.so
            libname = 'libpcap.so'

        try:
            self._libpcap = self._ffi.dlopen(libname)
        except Exception as e:
            raise PcapException("Error opening libpcap: {}".format(e))

        self._interfaces = []
        self.discoverdevs()

    @staticmethod
    def instance():
        if not _PcapFfi._instance:
            _PcapFfi._instance = _PcapFfi()
        return _PcapFfi._instance

    @property
    def version(self):
        return self._ffi.string(self._libpcap.pcap_lib_version())

    def discoverdevs(self):
        '''
        Find all the pcap-eligible devices on the local system.
        '''
        if len(self._interfaces):
            raise PcapException("Device discovery should only be done once.")

        ppintf = self._ffi.new("pcap_if_t * *")
        errbuf = self._ffi.new("char []", 128)
        rv = self._libpcap.pcap_findalldevs(ppintf, errbuf)
        if rv:
            raise PcapException("pcap_findalldevs returned failure: {}".format(self._ffi.string(errbuf)))
        pintf = ppintf[0]
        tmp = pintf
        pindex = 0
        while tmp != self._ffi.NULL:
            xname = self._ffi.string(tmp.name)  # "internal name"; still stored as bytes object
            xname = xname.decode('ascii', 'ignore')

            if self._windoze:
                ext_name = "port{}".format(pindex)
            else:
                ext_name = xname
            pindex += 1

            if tmp.description == self._ffi.NULL:
                xdesc = ext_name
            else:
                xdesc = self._ffi.string(tmp.description)
                xdesc = xdesc.decode('ascii', 'ignore')

            # NB: on WinPcap, only loop flag is set
            isloop = (tmp.flags & 0x1) == 0x1
            isup = (tmp.flags & 0x2) == 0x2
            isrunning = (tmp.flags & 0x4) == 0x4
            xif = PcapInterface(ext_name, xname, xdesc, isloop, isup, isrunning)
            self._interfaces.append(xif)

            tmp = tmp.next
        self._libpcap.pcap_freealldevs(pintf)

    @property
    def devices(self):
        return self._interfaces

    @property
    def lib(self):
        return self._libpcap

    @property
    def ffi(self):
        return self._ffi

    def _process_packet(self, xdev, header, packet, decode_tunnels=True):
        # MPLS header
        mpls = self._ffi.new("union mpls *")
        # IP header
        iph = self._ffi.new("struct nfstream_iphdr *")
        # IPv6 header
        iph6 = self._ffi.new("struct nfstream_ipv6hdr *")
        # lengths and offsets
        eth_offset = 0
        radio_len = 0
        fc = 0
        type = 0
        wifi_len = 0
        pyld_eth_len = 0
        check = 0
        ip_offset = 0
        ip_len = 0
        frag_off = 0
        vlan_id = 0
        proto = 0
        time = 0
        time = (header.tv_sec * TICK_RESOLUTION) + (header.tv_usec / (1000000 / TICK_RESOLUTION))

        datalink_type = self._libpcap.pcap_datalink(xdev)
        datalink_check = True
        while datalink_check:
            datalink_check = False
            if Dlt(datalink_type) == Dlt.DLT_NULL:
                tmp_dlt_null = self._ffi.cast('struct pp_32 *', packet + eth_offset)
                if int(ntohs(tmp_dlt_null.value)) == 2:
                    type = 0x0800
                else:
                    type = 0x86dd
                ip_offset = 4 + eth_offset
            elif Dlt(datalink_type) == Dlt.DLT_PPP_SERIAL:  # Cisco PPP in HDLC - like framing - 50
                chdlc = self._ffi.cast('struct nfstream_chdlc *', packet + eth_offset)
                ip_offset = self._ffi.sizeof('struct nfstream_chdlc')  # CHDLC_OFF = 4
                type = ntohs(chdlc.proto_code)
            elif (Dlt(datalink_type) == Dlt.DLT_C_HDLC) or (Dlt(datalink_type) == Dlt.DLT_PPP):  # Cisco PPP - 9 or 104
                chdlc = self._ffi.cast('struct nfstream_chdlc *', packet + eth_offset)  # CHDLC_OFF = 4
                ip_offset = self._ffi.sizeof('struct nfstream_chdlc')  # CHDLC_OFF = 4
                type = ntohs(chdlc.proto_code)
            elif Dlt(datalink_type) == Dlt.DLT_EN10MB:  # IEEE 802.3 Ethernet - 1 */
                ethernet = self._ffi.cast('struct nfstream_ethhdr *', packet + eth_offset)
                ip_offset = self._ffi.sizeof('struct nfstream_ethhdr') + eth_offset
                check = ntohs(ethernet.h_proto)
                if check <= 1500:
                    pyld_eth_len = check
                elif check >= 1536:
                    type = check

                if pyld_eth_len != 0:
                    llc = self._ffi.cast('struct nfstream_llc_header_snap *', packet + ip_offset)
                    if (llc.dsap == 0xaa) or (llc.ssap == 0xaa):  # check for LLC layer with SNAP ext
                        type = llc.snap.proto_ID
                        ip_offset += 8
                    elif (llc.dsap == 0x42) or (llc.ssap == 0x42):  # No SNAP ext
                        return None
            elif Dlt(datalink_type) == Dlt.DLT_LINUX_SLL:  # Linux Cooked Capture - 113
                type = (packet[eth_offset+14] << 8) + packet[eth_offset+15]
                ip_offset = 16 + eth_offset
            elif Dlt(datalink_type) == Dlt.DLT_IEEE802_11_RADIO:  # Radiotap link - layer - 127
                radiotap = self._ffi.cast('struct nfstream_radiotap_header *', packet + eth_offset)
                radio_len = radiotap.len
                if (radiotap.flags & self._ffi.BAD_FCS) == self._ffi.BAD_FCS:  # Check Bad FCS presence
                    return None
                # Calculate 802.11 header length(variable)
                wifi = self._ffi.cast('struct nfstream_wifi_header *', packet + eth_offset + radio_len)
                fc = wifi.fc
                # Check wifi data presence
                if fcf_type(fc) == 0x2:
                    if (fcf_to_ds(fc) and fcf_from_ds(fc) == 0x0) or\
                            (fcf_to_ds(fc) == 0x0 and fcf_from_ds(fc)):
                        wifi_len = 26  # + 4 byte fcs
                else:
                    pass
                # Check ether_type from LLC
                llc = self._ffi.cast('struct nfstream_llc_header_snap *', packet + (eth_offset + wifi_len + radio_len))
                if llc.dsap == self._ffi.SNAP:
                    type = ntohs(llc.snap.proto_ID)
                # Set IP header offset
                ip_offset = wifi_len + radio_len + self._ffi.sizeof('struct nfstream_llc_header_snap') + eth_offset
            elif Dlt(datalink_type) == Dlt.DLT_RAW:
                ip_offset = 0
                eth_offset = 0
            else:
                return None

            if type == 0x8100:
                vlan_id = ((packet[ip_offset] << 8) + packet[ip_offset + 1]) & 0xFFF
                type = (packet[ip_offset + 2] << 8) + packet[ip_offset + 3]
                ip_offset += 4
                if type == 0x8100:  # Double tagging for 802.1Q
                    vlan_id = ((packet[ip_offset] << 8) + packet[ip_offset + 1]) & 0xFFF
                    type = (packet[ip_offset + 2] << 8) + packet[ip_offset + 3]
                    ip_offset += 4
            elif (type == 0x8847) or (type == 0x8848):
                tmp_u32 = self._ffi.cast('struct pp_32 *', packet + ip_offset)
                mpls.u32 = int(ntohl(tmp_u32.value))
                type = 0x0800
                ip_offset += 4
                while not mpls.mpls.s:
                    tmp_u32_loop = self._ffi.cast('struct pp_32 *', packet + ip_offset)
                    mpls.u32 = int(ntohl(tmp_u32_loop.value))
                    ip_offset += 4
            elif type == 0x8864:
                type = 0x0800
                ip_offset += 8
            else:
                pass
            ip_check = True
            while ip_check:
                ip_check = False
                # Check and set IP header size and total packet length
                iph = self._ffi.cast('struct nfstream_iphdr *', packet + ip_offset)
                # Just work on Ethernet packets that contain IP
                if (type == 0x0800) and (header.caplen >= ip_offset):
                    frag_off = ntohs(iph.frag_off)
                    proto = iph.protocol
                    if header.caplen < header.len:
                        pass
                if iph.version == 4:
                    ip_len = iph.ihl * 4
                    iph6 = self._ffi.NULL
                    if iph.protocol == 41:  # IPPROTO_IPV6
                        ip_offset += ip_len
                        ip_check = True
                    if (frag_off & 0x1FFF) != 0:
                        return None
                elif iph.version == 6:
                    iph6 = self._ffi.cast('struct nfstream_ipv6hdr *', packet + ip_offset)
                    proto = iph6.ip6_hdr.ip6_un1_nxt
                    ip_len = self._ffi.sizeof('struct nfstream_ipv6hdr')
                    if proto == 60:  # IPv6 destination option
                        # options = self._ffi.new("uint8_t *")
                        options = self._ffi.cast('uint8_t *', packet + (ip_offset + ip_len))
                        proto = options[0]
                        ip_len += 8 * (options[1] + 1)
                    iph = self._ffi.NULL
                else:
                    return None

            if decode_tunnels and proto == 17:
                udp = self._ffi.new("struct nfstream_udphdr *")
                udp = self._ffi.cast('struct nfstream_udphdr *', packet + (ip_offset + ip_len))
                sport = self._ffi.new("uint16_t *")
                sport = int(ntohs(udp.source))
                dport = self._ffi.new("uint16_t *")
                dport = int(ntohs(udp.dest))
                if (sport == 2152) or (dport == 2152):
                    # Check if it's GTPv1
                    offset = ip_offset + ip_len + self._ffi.sizeof('struct nfstream_udphdr')
                    flags = packet[offset]
                    message_type = packet[offset + 1]
                    if (((flags & 0xE0) >> 5) == 1) and (message_type == 0xFF):
                        ip_offset = ip_offset + ip_len + self._ffi.sizeof('struct nfstream_udphdr') + 8  # GTPv1 header len
                        if flags & 0x04:
                            ip_offset += 1  # next_ext_header is present
                        if flags & 0x02:
                            ip_offset += 4  # sequence_number is present (it also includes next_ext_header and pdu_number)
                        if flags & 0x01:
                            ip_offset += 1 # pdu_number is present
                        iph = self._ffi.cast('struct nfstream_iphdr *', packet + ip_offset)
                        if iph.version == 4:
                            return None
                elif (sport == 37008) or (dport == 37008):
                    offset = ip_offset + ip_len + self._ffi.sizeof('struct nfstream_udphdr')
                    tzsp = self._ffi.cast('struct tzsp_header *', packet + offset)
                    version = int(ntohs(tzsp.version))
                    ts_type = int(ntohs(tzsp.type))
                    encapsulated_protocol = int(ntohs(tzsp.encapsulated_protocol))
                    if (version == 1) and (ts_type == 0) and (encapsulated_protocol == 1):
                        stop = 0
                        offset += 4
                        while (not stop) and (offset < header.caplen):
                            tag_type = packet[offset]
                            tag_len= 0
                            if tag_type == 0: # Padding tag
                                tag_len = 1
                            elif tag_type == 1: # End tag
                                tag_len = 1
                                stop = 1
                            else:
                                tag_len = packet[offset + 1]
                        offset += tag_len
                        if offset >= header.caplen:
                            return None  # Invalid packet
                        else:
                            eth_offset = offset
                            datalink_check = True

        l4_offset = 0
        ipsize = 0
        src_addr = 0
        dst_addr = 0
        l4_packet_len = 0
        version = 0
        if iph6 == self._ffi.NULL:
            version = 4
            l4_packet_len = ntohs(iph.tot_len) - (iph.ihl * 4)
            ipsize = header.caplen - ip_offset
            proto = iph.protocol
            src_addr = ntohl(iph.saddr)
            dst_addr = ntohl(iph.daddr)
        else:
            version = 6
            src_addr = ntohl(iph6.ip6_src.u6_addr.u6_addr32[0]) << 96 | ntohl(iph6.ip6_src.u6_addr.u6_addr32[1]) << 64 | ntohl(iph6.ip6_src.u6_addr.u6_addr32[2]) << 32 | ntohl(iph6.ip6_src.u6_addr.u6_addr32[3])
            dst_addr = ntohl(iph6.ip6_dst.u6_addr.u6_addr32[0]) << 96 | ntohl(iph6.ip6_dst.u6_addr.u6_addr32[1]) << 64 | ntohl(iph6.ip6_dst.u6_addr.u6_addr32[2]) << 32 | ntohl(iph6.ip6_dst.u6_addr.u6_addr32[3])
            proto = iph6.ip6_hdr.ip6_un1_nxt
            if proto == 60:
                options = self._ffi.cast('uint8_t *', iph6) + self._ffi.sizeof('struct nfstream_ipv6hdr')
                proto = options[0]
            l4_packet_len = ntohs(iph6.ip6_hdr.ip6_un1_plen)

        if version == 4:
            if ipsize < 20:
                return None
            if ((iph.ihl * 4) > ipsize) or (ipsize < ntohs(iph.tot_len)):
                return None
            l4_offset = iph.ihl * 4
            l3 = self._ffi.cast('uint8_t *', iph)
        else:
            l4_offset = self._ffi.sizeof('struct nfstream_ipv6hdr')
            l3 = self._ffi.cast('uint8_t *', iph6)

        l4 = self._ffi.cast('uint8_t *', l3) + l4_offset

        if (proto == 6) and l4_packet_len >= self._ffi.sizeof('struct nfstream_tcphdr'):
            tcph = self._ffi.cast('struct nfstream_tcphdr *', l4)
            sport = int(ntohs(tcph.source))
            dport = int(ntohs(tcph.dest))
        elif (proto == 17) and l4_packet_len >= self._ffi.sizeof('struct nfstream_udphdr'):
            udph = self._ffi.cast('struct nfstream_udphdr *', l4)
            sport = int(ntohs(udph.source))
            dport = int(ntohs(udph.dest))
        else:
            sport = 0
            dport = 0
        if version == 4:
            return PacketInformation(timestamp=time,
                                     capture_length=header.caplen,
                                     length=header.len,
                                     hash = nfstream_hash(src_addr, dst_addr, sport, dport, vlan_id, proto),
                                     ip_src_int=src_addr,
                                     ip_dst_int=dst_addr,
                                     src_port=sport,
                                     dst_port=dport,
                                     ip_protocol=proto,
                                     vlan_id=vlan_id,
                                     version=version,
                                     raw=bytes(xffi.buffer(iph, ipsize)))
        else:
            return PacketInformation(timestamp=time,
                                     capture_length=header.caplen,
                                     length=header.len,
                                     hash = nfstream_hash(src_addr, dst_addr, sport, dport, vlan_id, proto),
                                     ip_src_int=src_addr,
                                     ip_dst_int=dst_addr,
                                     src_port=sport,
                                     dst_port=dport,
                                     ip_protocol=proto,
                                     vlan_id=vlan_id,
                                     version=version,
                                     raw=bytes(xffi.buffer(iph6, header.len - ip_offset)))

    def _recv_packet(self, xdev):
        phdr = self._ffi.new("struct pcap_pkthdr **")
        pdata = self._ffi.new("unsigned char **")
        rv = self._libpcap.pcap_next_ex(xdev, phdr, pdata)
        if rv == 1:
            return self._process_packet(xdev, phdr[0], pdata[0], True)
        elif rv == 0:
            # timeout; nothing to return
            return 0
        elif rv == -1:
            # error on receive; raise an exception
            s = self._ffi.string(self._libpcap.pcap_geterr(xdev))
            raise PcapException("Error receiving packet: {}".format(s))
        elif rv == -2:
            # reading from savefile, but none left
            return -2

    def _set_filter(self, xdev, filterstr):
        bpf = self._ffi.new("struct bpf_program *")
        cfilter = self._ffi.new("char []", bytes(filterstr, 'ascii'))
        compile_result = self._libpcap.pcap_compile(xdev, bpf, cfilter, 0, 0xffffffff)
        if compile_result < 0:
            # get error, raise exception
            s = self._ffi.string(self._libpcap.pcap_geterr(xdev))
            raise PcapException("Error compiling filter expression: {}".format(s))

        sf_result = self._libpcap.pcap_setfilter(xdev, bpf)
        if sf_result < 0:
            # get error, raise exception
            s = self._ffi.string(self._libpcap.pcap_geterr(xdev))
            raise PcapException("Error setting filter on pcap handle: {}".format(s))
        self._libpcap.pcap_freecode(bpf)


def pcap_devices():
    return _PcapFfi.instance().devices


class PcapDumper(object):
    __slots__ = ['_ffi', '_libpcap', '_base', '_dumper']

    def __init__(self, outfile, dltype=Dlt.DLT_EN10MB, snaplen=65535):
        self._base = _PcapFfi.instance()
        self._ffi = self._base.ffi
        self._libpcap = self._base.lib
        pcap = self._libpcap.pcap_open_dead(dltype.value, snaplen)
        xoutfile = self._ffi.new("char []", bytes(outfile, 'ascii'))
        pcapdump = self._libpcap.pcap_dump_open(pcap, xoutfile)
        dl = self._libpcap.pcap_datalink(pcap)
        snaplen = self._libpcap.pcap_snapshot(pcap)
        self._dumper = PcapDev(Dlt(dl), 0, snaplen, _PcapFfi.instance().version, pcapdump)

    def write_packet(self, pkt, ts=None):
        if not isinstance(pkt, bytes):
            raise PcapException("Packet to be written needs to be a Python bytes object")
        pkthdr = self._ffi.new("struct pcap_pkthdr *")
        if not ts:
            ts = time()

        pkthdr.tv_sec = int(ts)
        pkthdr.tv_usec = int(1000000 * (ts - int(ts)))

        pkthdr.caplen = len(pkt)
        pkthdr.len = len(pkt)
        xpkt = self._ffi.new("unsigned char []", pkt)
        self._libpcap.pcap_dump(self._dumper.pcap, pkthdr, xpkt)

    def close(self):
        self._libpcap.pcap_dump_close(self._dumper.pcap)


class PcapReader(object):
    '''
    Class the represents a reader of an existing pcap capture file.
    '''
    __slots__ = ['_ffi', '_libpcap', '_base', '_pcapdev', '_user_callback']

    def __init__(self, filename, filterstr=None):
        self._base = _PcapFfi.instance()
        self._ffi = self._base.ffi
        self._libpcap = self._base.lib
        self._user_callback = None

        errbuf = self._ffi.new("char []", 128)
        pcap = self._libpcap.pcap_open_offline(bytes(filename, 'ascii'), errbuf)
        if pcap == self._ffi.NULL:
            raise PcapException(
                "Failed to open pcap file for reading: {}: {}".format(filename, self._ffi.string(errbuf)))

        dl = self._libpcap.pcap_datalink(pcap)
        try:
            dl = Dlt(dl)
        except ValueError as e:
            raise PcapException("Don't know how to handle datalink type {}".format(dl))
        self._pcapdev = PcapDev(dl, 0, 0, _PcapFfi.instance().version, pcap)

        if filterstr is not None:
            self._base._set_filter(pcap, filterstr)

    def close(self):
        self._libpcap.pcap_close(self._pcapdev.pcap)

    def recv_packet(self):
        return self._base._recv_packet(self._pcapdev.pcap)

    def set_filter(self, filterstr):
        self._base._set_filter(self._pcapdev.pcap, filterstr)

    def dispatch(self, callback, count=-1):
        self._user_callback = callback
        handle = self._ffi.new_handle(self)
        rv = self._libpcap.pcap_dispatch(self._pcapdev.pcap, count, _pcap_callback, handle)
        return rv

    def loop(self, callback, count=-1):
        self._user_callback = callback
        handle = self._ffi.new_handle(self)
        rv = self._libpcap.pcap_loop(self._pcapdev.pcap, count, _pcap_callback, handle)
        return rv

    def _callback(self, pkt):
        self._user_callback(pkt)

    def breakloop(self):
        self._libpcap.pcap_breakloop(self._pcapdev.pcap)


class PcapLiveDevice(object):
    '''
    Class the represents a live pcap capture/injection device.
    '''
    _OpenDevices = {}  # objectid -> low-level pcap dev
    _lock = Lock()
    __slots__ = ['_ffi', '_libpcap', '_base', '_pcapdev', '_devname', '_fd', '_user_callback']

    def __init__(self, device, snaplen=65535, promisc=1, to_ms=100,
                 filterstr=None, nonblock=True, only_create=False):
        self._base = _PcapFfi.instance()
        self._ffi = self._base.ffi
        self._libpcap = self._base.lib
        self._fd = None
        self._user_callback = None

        errbuf = self._ffi.new("char []", 128)
        internal_name = None
        for dev in self._base._interfaces:
            if dev.name == device:
                internal_name = dev.internal_name
                break
        if internal_name is None:
            raise Exception("No such device {} exists.".format(device))
        self._devname = device
        self._pcapdev = None

        if only_create:
            pcap = self._libpcap.pcap_create(bytes(internal_name, 'ascii'), errbuf)
            self._pcapdev = PcapDev(0, 0, 0, _PcapFfi.instance().version, pcap)
            with PcapLiveDevice._lock:
                PcapLiveDevice._OpenDevices[id(self)] = pcap
            if pcap == self._ffi.NULL:
                raise PcapException("Failed to open live device {}: {}".format(internal_name, self._ffi.string(errbuf)))
            return

        pcap = self._libpcap.pcap_open_live(bytes(internal_name, 'ascii'), snaplen, promisc, to_ms, errbuf)
        if pcap == self._ffi.NULL:
            raise PcapException("Failed to open live device {}: {}".format(internal_name, self._ffi.string(errbuf)))

        if nonblock:
            rv = self._libpcap.pcap_setnonblock(pcap, 1, errbuf)
            if rv != 0:
                raise PcapException(
                    "Error setting pcap device in nonblocking state: {}".format(self._ffi.string(errbuf)))

        # gather what happened
        nblock = self._libpcap.pcap_getnonblock(pcap, errbuf)
        snaplen = self._libpcap.pcap_snapshot(pcap)
        dl = self._libpcap.pcap_datalink(pcap)
        try:
            dl = Dlt(dl)
        except ValueError as e:
            raise PcapException("Don't know how to handle datalink type {}".format(dl))

        self._pcapdev = PcapDev(dl, nblock, snaplen, _PcapFfi.instance().version, pcap)
        self._fd = self._libpcap.pcap_get_selectable_fd(self._pcapdev.pcap)

        with PcapLiveDevice._lock:
            PcapLiveDevice._OpenDevices[id(self)] = self._pcapdev.pcap

        if filterstr is not None:
            self.set_filter(filterstr)

    @staticmethod
    def create(device):
        return PcapLiveDevice(device, only_create=True)

    def activate(self):
        rv = self._libpcap.pcap_activate(self._pcapdev.pcap)
        if rv < 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error activating: {} {}".format(rv, s))

        warning = 0
        if rv > 0:
            warning = PcapWarning(rv)

        self._pcapdev = PcapDev(self.dlt, self.blocking, self.snaplen,
                                _PcapFfi.instance().version, self._pcapdev.pcap)
        return warning

    @property
    def blocking(self):
        errbuf = self._ffi.new("char []", 128)
        rv = self._libpcap.pcap_getnonblock(self._pcapdev.pcap, errbuf)
        if rv != 0:
            raise PcapException("Error getting nonblock state: {}".format(self._ffi.string(errbuf)))
        return bool(rv)

    @blocking.setter
    def blocking(self, value):
        errbuf = self._ffi.new("char []", 128)
        rv = self._libpcap.pcap_setnonblock(self._pcapdev.pcap, int(value), errbuf)
        if rv != 0:
            raise PcapException("Error setting nonblock state: {}".format(self._ffi.string(errbuf)))

    @property
    def snaplen(self):
        return self._libpcap.pcap_snapshot(self._pcapdev.pcap)

    @snaplen.setter
    def snaplen(self, value):
        rv = self._libpcap.pcap_set_snaplen(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting snaplen: {}".format(s))

    def set_promiscuous(self, value):
        rv = self._libpcap.pcap_set_promisc(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting promiscuous mode: {}".format(s))

    def set_timeout(self, value):
        rv = self._libpcap.pcap_set_timeout(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting timeout value: {}".format(s))

    def set_buffer_size(self, value):
        rv = self._libpcap.pcap_set_buffer_size(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting buffer size: {}".format(s))

    def set_immediate_mode(self, value):
        rv = self._libpcap.pcap_set_immediate_mode(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting immediate mode: {}".format(s))

    def list_tstamp_types(self):
        errbuf = self._ffi.new("char []", 128)
        ppint = self._ffi.new("int * *")
        rv = self._libpcap.pcap_list_tstamp_types(self._pcapdev.pcap, ppint)
        if rv < 0:
            raise PcapException("Error getting tstamp type list: {}".format(self._ffi.string(errbuf)))

        xints = ppint[0]
        tstamptypes = []
        for i in range(rv):
            tstamptypes.append(PcapTstampType(xints[i]))

        self._libpcap.pcap_free_tstamp_types(xints)
        return tstamptypes

    def set_tstamp_type(self, value):
        value = PcapTstampType(value)
        valid_types = self.list_tstamp_types()
        if value not in valid_types:
            raise PcapException("Not a valid tstamp type for this device (see list_tstamp_types)")
        rv = self._libpcap.pcap_set_tstamp_type(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting timestamp type: {}".format(s))

    @property
    def tstamp_precision(self):
        val = self._libpcap.pcap_get_tstamp_precision(self._pcapdev.pcap)
        return PcapTstampPrecision(val)

    @tstamp_precision.setter
    def tstamp_precision(self, value):
        value = PcapTstampPrecision(value)
        rv = self._libpcap.pcap_set_tstamp_precision(self._pcapdev.pcap, int(value))
        if rv != 0:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting timestamp precision: {}".format(s))

    @staticmethod
    def set_bpf_filter_on_all_devices(filterstr):
        '''
        Long method name, but self-explanatory.  Set the bpf
        filter on all devices that have been opened.
        '''
        with PcapLiveDevice._lock:
            for dev in PcapLiveDevice._OpenDevices.values():
                _PcapFfi.instance()._set_filter(dev, filterstr)

    @property
    def dlt(self):
        dl = self._libpcap.pcap_datalink(self._pcapdev.pcap)
        try:
            rv = Dlt(dl)
            return rv
        except:
            raise PcapException("Don't know how to handle datalink type {}".format(dl))

    @property
    def fd(self):
        if self._fd is not None:
            return self._fd
        try:
            fd = self._libpcap.pcap_get_selectable_fd(self._pcapdev.pcap)
            self._fd = fd
            return fd
        except:
            s = self._ffi.string(self._libpcap.pcap_geterr(xpcap))
            raise PcapException("Error getting select fd: {}".format(s))

    @property
    def name(self):
        return self._devname

    def send_packet(self, xbuffer):
        if not isinstance(xbuffer, bytes):
            raise PcapException("Packets to be sent via libpcap must be serialized as a bytes object")
        xlen = len(xbuffer)
        rv = self._libpcap.pcap_sendpacket(self._pcapdev.pcap, xbuffer, xlen)
        if rv == 0:
            return True
        s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
        raise PcapException("Error sending packet: {}".format(s))

    def recv_packet_or_none(self):
        return self._base._recv_packet(self._pcapdev.pcap)

    def dispatch(self, callback, count=-1):
        self._user_callback = callback
        handle = self._ffi.new_handle(self)
        rv = self._libpcap.pcap_dispatch(self._pcapdev.pcap, count, _pcap_callback, handle)
        return rv

    def loop(self, callback, count=-1):
        self._user_callback = callback
        handle = self._ffi.new_handle(self)
        rv = self._libpcap.pcap_loop(self._pcapdev.pcap, count, _pcap_callback, handle)
        return rv

    def _callback(self, pkt):
        self._user_callback(pkt)

    def breakloop(self):
        self._libpcap.pcap_breakloop(self._pcapdev.pcap)

    def recv_packet(self, timeout=None):
        if timeout is None or timeout < 0:
            timeout = None
        if self._fd >= 0:
            try:
                xread, xwrite, xerr = select([self._fd], [], [self._fd], timeout)
            except PcapException:
                return None
            if xread:
                return self._base._recv_packet(self._pcapdev.pcap)
            # timeout; return nothing
            return None
        elif self._pcapdev.nonblock:
            # can't do select, but we're in nonblocking mode so sleep
            # up to 10 times before giving up, all while respecting the
            # timeout value
            if timeout:
                now = time()
                expiry = now + timeout
                while now < expiry:
                    sleep(timeout / 10)
                    pkt = self._base._recv_packet(self._pcapdev.pcap)
                    if pkt:
                        return pkt
                    now = time()
                # after all that, still got nothing.
                return None
            else:
                return self._base._recv_packet(self._pcapdev.pcap)
        else:
            # no select, no non-blocking mode.  block away, my friend.
            return self._base._recv_packet(self._pcapdev.pcap)

    def close(self):
        with PcapLiveDevice._lock:
            xid = id(self)
            del PcapLiveDevice._OpenDevices[xid]
        self._libpcap.pcap_close(self._pcapdev.pcap)

    def stats(self):
        pstat = self._ffi.new("struct pcap_stat *")
        rv = self._libpcap.pcap_stats(self._pcapdev.pcap, pstat)
        if rv == 0:
            return PcapStats(pstat.recv, pstat.drop, pstat.ifdrop)
        else:
            s = self._ffi.string(self._libpcap.pcap_geterr(xpcap))
            raise PcapException("Error getting stats: {}".format(s))

    def set_filter(self, filterstr):
        self._base._set_filter(self._pcapdev.pcap, filterstr)

    def set_direction(self, direction):
        rv = self._libpcap.pcap_setdirection(self._pcapdev.pcap, int(direction))
        if rv == 0:
            return
        else:
            s = self._ffi.string(self._libpcap.pcap_geterr(self._pcapdev.pcap))
            raise PcapException("Error setting direction: {}".format(s))


_PcapFfi()  # instantiate singleton
xffi = _PcapFfi.instance().ffi


@xffi.callback("void(*)(unsigned char *, const struct pcap_pkthdr *, const unsigned char *)")
def _pcap_callback(handle, phdr, pdata):
    xhandle = xffi.cast("void *", handle)
    pcapobj = xffi.from_handle(xhandle)
    rawpkt = bytes(xffi.buffer(pdata, phdr[0].caplen))
    # dt = datetime.fromtimestamp(phdr[0].tv_sec)
    usec = int(xffi.cast("int", phdr[0].tv_usec))
    # ts = dt.replace(microsecond=usec)
    ts = float("{}.{:06d}".format(phdr[0].tv_sec, usec))
    pkt = PcapPacket(ts, phdr[0].caplen, phdr[0].len, rawpkt)
    pcapobj._callback(pkt)


def check_source_type(source):
    if source is None:  # start on first up device
        for dev in pcap_devices():
            if dev.isup:
                print("Streamer source not defined. Set to interface {} as default value.".format(dev.name))
                return dev.name, 1
        raise OSError
    if os.path.isfile(str(source)):
        return str(source), 0
    else:  # check if valid device.
        for dev in pcap_devices():
            if str(source) == dev.name:
                return str(source), 1
    raise OSError("Streamer initialized on unfound source: {}".format(str(source)))


class Observer:
    def __init__(self, source=None, snaplen=65535, promisc=1, to_ms=0, filter_str=None, non_block=True):
        source_type = check_source_type(source)
        if source_type[1] == 1:  # Live interface
            try:
                self.packet_generator = PcapLiveDevice(device=source, snaplen=snaplen, promisc=promisc, to_ms=to_ms,
                                                       filterstr=filter_str, nonblock=non_block)
            except PcapException:
                raise OSError("Root privilege needed for live capture on {} interface.".format(source))
        elif source_type[1] == 0:  # pcap case
            try:
                self.packet_generator = PcapReader(filename=source, filterstr=filter_str)
            except PcapException:
                raise OSError('Unable to read pcap format of: {}'.format(source))
        else:
            self.packet_generator = None

    def __iter__(self):
        if self.packet_generator is not None:
            try:
                while True:
                    try:
                        r = self.packet_generator.recv_packet()
                        if r is None:
                            pass
                        elif r == -2:
                            return
                        elif r == 0:
                            pass
                        else:
                            yield r
                    except PcapException:
                        pass
            except KeyboardInterrupt:
                return
