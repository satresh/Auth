class CompanyRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'company1_products':
            return 'company1'
        elif model._meta.app_label == 'company2_products':
            return 'company2'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'company1_products':
            return 'company1'
        elif model._meta.app_label == 'company2_products':
            return 'company2'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'company1_products':
            return db == 'company1'
        elif app_label == 'company2_products':
            return db == 'company2'
        return None