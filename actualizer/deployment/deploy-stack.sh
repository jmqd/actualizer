STACK=`cat stack.json`
STACK_NAME="actualizer-us-west-2-prod-stack"

aws cloudformation update-stack --stack-name "$STACK_NAME" --template-body "$STACK"
