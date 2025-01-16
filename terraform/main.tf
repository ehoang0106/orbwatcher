resource "aws_dynamodb_table" "orbwatcher" {
  name           = "orbwatcher"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "date"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "currency-name"
    type = "S"
  }

  attribute {
    name = "price-value"
    type = "N"
  }

  attribute {
    name = "exchange-price-value"
    type = "N"
  }

  global_secondary_index {
    name            = "CurrencyNameIndex"
    hash_key        = "currency-name"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }

  global_secondary_index {
    name            = "PriceValueIndex"
    hash_key        = "price-value"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }

  global_secondary_index {
    name            = "ExchangePriceValueIndex"
    hash_key        = "exchange-price-value"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }
}


