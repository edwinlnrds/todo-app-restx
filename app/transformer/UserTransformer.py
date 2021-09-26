from app.transformer.BaseTransformer import BaseTransformer

class UserTransformer(BaseTransformer):
    @staticmethod
    def single_transform(value: object):
        return {
            'id': str(value.id),
            'name': value.name,
            'email': value.email,
            'created_at': str(value.created_at),
            'last_updated': str(value.last_updated)
        }