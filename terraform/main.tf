resource "aws_dynamodb_table" "orbwatcher" {
  name           = "orbwatcher"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = date

  attribute {
    name = "date"
    type = "S"
  }
}