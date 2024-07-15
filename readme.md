python3 ./output_exports.py > exports.sh
source exports.sh
rm exports.sh

terraform -chdir=../testSubAction-Code/pre init -backend-config="key=SubscriptionCreation/${TF_VAR_resource_group_name}/pre/terraform.tfstate"
terraform -chdir=../testSubAction-Code/post init -backend-config="key=SubscriptionCreation/${TF_VAR_resource_group_name}/post/terraform.tfstate"

python3 ./output_exports.py True