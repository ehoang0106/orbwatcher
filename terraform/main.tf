resource "aws_dynamodb_table" "orbwatcher" {
  name           = "orbwatcher"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "currency_id"
  range_key = "date"

  attribute {
    name = "currency_id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }
}