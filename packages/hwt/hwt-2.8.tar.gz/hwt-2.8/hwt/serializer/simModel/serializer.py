from copy import copy
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.process import HWProcess
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.typeCast import toHVal
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.constCache import ConstCache
from hwt.serializer.generic.context import SerializerCtx
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.nameScope import LangueKeyword
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.simModel.keywords import SIMMODEL_KEYWORDS
from hwt.serializer.simModel.ops import SimModelSerializer_ops
from hwt.serializer.simModel.types import SimModelSerializer_types
from hwt.serializer.simModel.value import SimModelSerializer_value
from hwt.serializer.utils import maxStmId
from ipCorePackager.constants import DIRECTION


env = Environment(loader=PackageLoader('hwt', 'serializer/simModel/templates'))
unitTmpl = env.get_template('modelCls.py.template')
processTmpl = env.get_template('process.py.template')
ifTmpl = env.get_template("if.py.template")


def sensitivityByOp(op):
    """
    get sensitivity type for operator
    """
    if op == AllOps.RISING_EDGE:
        return (True, False)
    elif op == AllOps.FALLING_EDGE:
        return (False, True)
    else:
        raise TypeError()


class SimModelSerializer(SimModelSerializer_value, SimModelSerializer_ops,
                         SimModelSerializer_types, GenericSerializer):
    """
    Serializer which converts Unit instances to simulator code
    """
    _keywords_dict = {kw: LangueKeyword() for kw in SIMMODEL_KEYWORDS}
    fileExtension = '.py'

    @classmethod
    def serializationDecision(cls, obj, serializedClasses,
                              serializedConfiguredUnits):
        # we need all instances for simulation
        return True

    @classmethod
    def stmAsHdl(cls, obj, ctx: SerializerCtx):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, ctx)

    @classmethod
    def Architecture(cls, arch: Architecture, ctx: SerializerCtx):
        cls.Entity_prepare(arch.entity, ctx, serialize=False)
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        ports = list(
            map(lambda p: (p.name, cls.HdlType(p._dtype, ctx)),
                arch.entity.ports))

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, HEnum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(
                    cls.HdlType(t, ctx, declaration=True))

            v.name = ctx.scope.checkedName(v.name, v)
            variables.append(v)

        childCtx = copy(ctx)
        childCtx.constCache = ConstCache(ctx.scope.checkedName)

        def serializeVar(v):
            dv = v.def_val
            if isinstance(dv, HEnumVal):
                dv = "self.%s.%s" % (dv._dtype.name, dv.val)
            else:
                dv = cls.Value(dv, ctx)

            return v.name, cls.HdlType(v._dtype, childCtx), dv

        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        constants = []
        for c in sorted(childCtx.constCache._cache.items(), key=lambda x: x[1],
                        reverse=True):
            constants.append((c[1], cls.Value(c[0], ctx)))

        return unitTmpl.render(
            DIRECTION=DIRECTION,
            name=arch.getEntityName(),
            constants=constants,
            ports=ports,
            signals=list(map(serializeVar, variables)),
            extraTypes=extraTypes_serialized,
            processes=procs,
            processObjects=arch.processes,
            processesNames=map(lambda p: p.name, arch.processes),
            componentInstances=arch.componentInstances,
            isOp=lambda x: isinstance(x, Operator),
            sensitivityByOp=sensitivityByOp,
            serialize_io=cls.sensitivityListItem,
        )

    @classmethod
    def Assignment(cls, a: Assignment, ctx: SerializerCtx):
        dst = a.dst
        indentStr = getIndent(ctx.indent)
        ev = a._is_completly_event_dependent

        srcStr = "%s" % cls.Value(a.src, ctx)
        if a.indexes is not None:
            return "%sself.io.%s.val_next = (%s, (%s,), %s)" % (
                indentStr, dst.name, srcStr,
                ", ".join(map(lambda x: cls.asHdl(x, ctx),
                              a.indexes)),
                ev)
        else:
            if not (dst._dtype == a.src._dtype):
                srcT = a.src._dtype
                dstT = dst._dtype
                if (isinstance(srcT, Bits) and
                        isinstance(dstT, Bits)):
                    bl0 = srcT.bit_length()
                    if bl0 == dstT.bit_length():
                        if bl0 == 1 and srcT.force_vector != dstT.force_vector:
                            _0 = cls.Value(toHVal(0), ctx)
                            if srcT.force_vector:
                                return "%sself.io.%s.val_next = ((%s)[%s], %s)"\
                                    % (indentStr, dst.name, srcStr, _0, ev)
                            else:
                                return "%sself.io.%s.val_next = (%s, (%s,), %s)" % (
                                    indentStr, dst.name, srcStr, _0, ev)
                        elif srcT.signed == dstT.signed:
                            return "%sself.io.%s.val_next = (%s, %s)" % (
                                    indentStr, dst.name, srcStr, ev)

                raise SerializerException(
                    ("%s <= %s  is not valid assignment\n"
                     " because types are different (%r; %r) ") %
                    (cls.asHdl(dst, ctx), srcStr,
                     dst._dtype, a.src._dtype))
            else:
                return "%sself.io.%s.val_next = (%s, %s)" % (
                    indentStr, dst.name, srcStr, ev)

    @classmethod
    def comment(cls, comentStr: str):
        return "#" + comentStr.replace("\n", "\n#")

    @classmethod
    def IfContainer(cls, ifc: IfContainer, ctx: SerializerCtx):
        cond = cls.condAsHdl(ifc.cond, ctx)
        ifTrue = ifc.ifTrue

        if ifc.elIfs:
            # replace elifs with nested if statements
            ifFalse = []
            topIf = IfContainer(ifc.cond, ifc.ifTrue, ifFalse)
            topIf._inputs = ifc._inputs
            topIf._outputs = ifc._outputs
            topIf._sensitivity = ifc._sensitivity

            for c, stms in ifc.elIfs:
                _ifFalse = []

                lastIf = IfContainer(c, stms, _ifFalse)
                lastIf._inputs = ifc._inputs
                lastIf._outputs = ifc._outputs
                lastIf._sensitivity = ifc._sensitivity

                ifFalse.append(lastIf)
                ifFalse = _ifFalse

            if ifc.ifFalse is None:
                lastIf.ifFalse = []
            else:
                lastIf.ifFalse = ifc.ifFalse

            return cls.IfContainer(topIf, ctx)
        else:
            ifFalse = ifc.ifFalse
            if ifFalse is None:
                ifFalse = []

            childCtx = ctx.withIndent()
            outputInvalidateStms = []
            for o in ifc._outputs:
                # [TODO] look up indexes
                indexes = None
                oa = Assignment(o._dtype.from_py(None), o, indexes,
                                virtual_only=True, parentStm=ifc,
                                is_completly_event_dependent=ifc._is_completly_event_dependent)
                outputInvalidateStms.append(cls.stmAsHdl(oa, childCtx))

            return ifTmpl.render(
                indent=getIndent(ctx.indent),
                indentNum=ctx.indent,
                cond=cond,
                outputInvalidateStms=outputInvalidateStms,
                ifTrue=tuple(map(
                    lambda obj: cls.stmAsHdl(obj, childCtx),
                    ifTrue)),
                ifFalse=tuple(map(
                    lambda obj: cls.stmAsHdl(obj, childCtx),
                    ifFalse)))

    @classmethod
    def SwitchContainer(cls, sw: SwitchContainer,
                        ctx: SerializerCtx):
        switchOn = sw.switchOn

        def mkCond(c):
            return switchOn._eq(c)

        elIfs = []

        for key, statements in sw.cases[1:]:
            elIfs.append((mkCond(key), statements))
        ifFalse = sw.default

        topCond = mkCond(sw.cases[0][0])
        topIf = IfContainer(topCond,
                            ifTrue=sw.cases[0][1],
                            ifFalse=ifFalse,
                            elIfs=elIfs)

        topIf._sensitivity = sw._sensitivity
        topIf._inputs = sw._inputs
        topIf._outputs = sw._outputs

        return cls.IfContainer(topIf, ctx)

    @classmethod
    def sensitivityListItem(cls, item):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = (True, False)
            elif op == AllOps.FALLING_EDGE:
                sens = (False, True)
            else:
                raise TypeError("This is not an event sensitivity", op)

            return "(%s, %s)" % (str(sens), item.operands[0].name)
        else:
            return item.name

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx: SerializerCtx):
        body = proc.statements
        assert body
        proc.name = ctx.scope.checkedName(proc.name, proc)
        sensitivityList = sorted(
            map(cls.sensitivityListItem, proc.sensitivityList))

        childCtx = ctx.withIndent(2)
        _body = "\n".join([
            cls.stmAsHdl(stm, childCtx)
            for stm in body])

        return processTmpl.render(
            hasConditions=arr_any(
                body, lambda stm: not isinstance(stm, Assignment)),
            name=proc.name,
            sensitivityList=sensitivityList,
            stmLines=[_body]
        )
