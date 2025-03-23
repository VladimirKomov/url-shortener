class ValidationKafkaMapper:
    @staticmethod
    def to_kafka_message(short_code: str, original_url: str) -> dict:
        return {
            "short_code": short_code,
            "original_url": original_url,
        }

    @staticmethod
    def from_kafka_result(message: dict) -> tuple[str, bool]:
        return message["short_code"], message["is_valid"]
