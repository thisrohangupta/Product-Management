package namespace_validation


deny[msg] {
    not contains(allowed, input.infrastructureNamespace)
	msg := sprintf("Infrastructure namespace '%s' is not allowed", [input.infrastructureNamespace])
}

# Deny pipelines if the namespace is missing completely
deny["No namespace defined for the infrastructure"] {
	not input.infrastructureNamespace
}

# Namespaces that can be used for service
## They want this to be an expression rather than hard coded into the policy, we do not evaluate expressions within the rego - thus enhancement

allowed = ["dev", "default"] 
contains(arr, elem) {
	arr[_] = elem
}
