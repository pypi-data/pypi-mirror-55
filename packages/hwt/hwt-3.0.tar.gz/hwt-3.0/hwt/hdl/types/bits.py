from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.serializer.generic.indent import getIndent
from pyMathBitPrecise.bits3t import Bits3t


BITS_DEFAUTL_SIGNED = None
BITS_DEFAUTL_FORCEVECTOR = False
BITS_DEFAUTL_NEGATED = False


class Bits(HdlType, Bits3t):
    """
    Elemental HDL type representing bits (vector or single bit)
    """

    def __init__(self, bit_length, signed=BITS_DEFAUTL_SIGNED,
                 force_vector=BITS_DEFAUTL_FORCEVECTOR,
                 negated=BITS_DEFAUTL_NEGATED,
                 name=None,
                 strict_sign=True, strict_width=True):
        """
        :param negated: if true the value is in negated form
        """
        self.negated = negated

        bit_length = int(bit_length)
        assert bit_length > 0
        Bits3t.__init__(self, bit_length, signed, name=name,
                        force_vector=force_vector,
                        strict_sign=strict_sign, strict_width=strict_width)

    @internal
    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return int(2 ** self.bit_length())

    @internal
    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.bitsCast import convertBits
        return convertBits

    @internal
    @classmethod
    def get_reinterpret_cast_fn(cls):
        from hwt.hdl.types.bitsCast import reinterpretBits
        return reinterpretBits

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.bitsVal import BitsVal
            cls._valCls = BitsVal
            return cls._valCls

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and HArray)
        """
        constr = []
        if self.name is not None:
            constr.append('"%s"' % self.name)
        c = self.bit_length()
        constr.append("%dbits" % c)
        if self.force_vector:
            constr.append("force_vector")
        if self.signed:
            constr.append("signed")
        elif self.signed is False:
            constr.append("unsigned")
        if not self.strict_sign:
            constr.append("strict_sign=False")
        if not self.strict_width:
            constr.append("strict_width=False")

        return "%s<%s, %s>" % (getIndent(indent),
                               self.__class__.__name__,
                               ", ".join(constr))
