from PyInquirer import Validator, ValidationError

class CountValidator(Validator):
    def validate(self, document):
        try:
            answer = int(document.text)
            if answer < 1 and not answer == -1:
                raise ValidationError(
                    message='Please enter a valid positive integer or -1',
                    cursor_position=len(document.text)
                )
        except ValueError:
            raise ValidationError(
                message='Please enter a valid positive integer or -1',
                cursor_position=len(document.text)
            )
