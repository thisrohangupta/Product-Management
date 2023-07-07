package pipeline

# Deny pipelines that do not use allowed environments
# NOTE: Try removing "test" from the 'allowed_environments' list to see the policy fail
deny[msg] {
	# Find all deployment stages
	stage = input.pipeline.stages[_].stage
	stage.type == "Deployment"

	# ... where the environment is not in the allow list
	not contains(allowed_environments, stage.spec.infrastructure.environment.identifier)

	# Show a human-friendly error message
	msg := sprintf("deployment stage '%s' cannot be deployed to environment '%s'", [stage.name, stage.spec.infrastructure.environment.identifier])
}

# Deny pipelines if the environment is missing completely
deny[msg] {
	# Find all deployment stages
	stage = input.pipeline.stages[_].stage
	stage.type == "Deployment"

	# ... without an environment
	not stage.spec.infrastructure.environment.identifier

	# Show a human-friendly error message
	msg := sprintf("deployment stage '%s' has no environment identifier", [stage.name])
}

# Environments that can be used for deployment
allowed_environments = ["k8s-dev","k8s-prod"]

contains(arr, elem) {
	arr[_] = elem
}
