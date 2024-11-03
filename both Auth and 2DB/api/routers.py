class CompanyRouter:
    def db_for_read(self, model, **hints):
        user = hints.get('user')
        if model._meta.app_label == 'api' and model.__name__ == 'Product':
            if user and hasattr(user, 'company'):
                return user.company
        return None

    def db_for_write(self, model, **hints):
        user = hints.get('user')
        if model._meta.app_label == 'api' and model.__name__ == 'Product':
            if user and hasattr(user, 'company'):
                return user.company
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'api' and model_name == 'product':
            return db in ['company1', 'company2']
        return None
