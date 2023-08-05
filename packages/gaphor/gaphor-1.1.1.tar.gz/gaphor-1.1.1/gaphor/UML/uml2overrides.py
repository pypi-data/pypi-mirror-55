import itertools


# See https://www.omg.org/spec/UML/2.5/PDF, section 12.4.1.5, page 271
def extension_metaclass(self):
    """
    References the Class that is extended through an Extension. The
    property is derived from the type of the memberEnd that is not the
    ownedEnd.
    """
    ownedEnd = self.ownedEnd
    metaend = [e for e in self.memberEnd if e is not ownedEnd]
    if metaend:
        return metaend[0].type


def property_opposite(self):
    """
    In the case where the property is one navigable end of a binary
    association with both ends navigable, this gives the other end.

    For Gaphor the property on the other end is returned regardless the
    navigability.
    """
    if self.association is not None and len(self.association.memberEnd) == 2:
        return (
            self.association.memberEnd[0] is self
            and self.association.memberEnd[1]
            or self.association.memberEnd[0]
        )
    return None


def property_navigability(self):
    """
    Get navigability of an association end.
    If no association is related to the property, then unknown navigability
    is assumed.
    """
    from gaphor.UML.uml2 import Class, Interface

    assoc = self.association
    if not assoc or not self.opposite:
        return None  # assume unknown
    owner = self.opposite.type
    if owner and (
        (type(self.type) in (Class, Interface) and self in owner.ownedAttribute)
        or self in assoc.navigableOwnedEnd
    ):
        return True
    elif self in assoc.ownedEnd:
        return None
    else:
        return False


def _pr_interface_deps(classifier, dep_type):
    """
    Return all interfaces, which are connected to a classifier with given
    dependency type.
    """
    from gaphor.UML.uml2 import Interface

    return (
        dep.supplier[0]
        for dep in classifier.clientDependency
        if dep.isKindOf(dep_type) and dep.supplier[0].isKindOf(Interface)
    )


def _pr_rc_interface_deps(component, dep_type):
    """
    Return all interfaces, which are connected to realizing classifiers of
    specified component. Returned interfaces are connected to realizing
    classifiers with given dependency type.

    Generator of generators is returned. Do not forget to flat it later.
    """
    return (
        _pr_interface_deps(r.realizingClassifier, dep_type)
        for r in component.realization
    )


def component_provided(self):
    """
    Interfaces provided to component environment.
    """
    from gaphor.UML.uml2 import Implementation, Realization

    implementations = (
        impl.contract[0]
        for impl in self.implementation
        if impl.isKindOf(Implementation)
    )
    realizations = _pr_interface_deps(self, Realization)

    # realizing classifiers realizations
    # this generator of generators, so flatten it later
    rc_realizations = _pr_rc_interface_deps(self, Realization)

    return tuple(set(itertools.chain(implementations, realizations, *rc_realizations)))


def component_required(self):
    """
    Interfaces required by component.
    """
    from gaphor.UML.uml2 import Usage

    usages = _pr_interface_deps(self, Usage)

    # realizing classifiers usages
    # this generator of generators, so flatten it later
    rc_usages = _pr_rc_interface_deps(self, Usage)

    return tuple(set(itertools.chain(usages, *rc_usages)))


def message_messageKind(self):
    """
    MessageKind
    """
    kind = "unknown"
    if self.sendEvent:
        kind = "lost"
        if self.receiveEvent:
            kind = "complete"
    elif self.receiveEvent:
        kind = "found"
    return kind


def namedelement_qualifiedname(self):
    """
    Returns the qualified name of the element as a tuple
    """
    if self.namespace:
        return self.namespace.qualifiedName + (self.name,)
    else:
        return (self.name,)
