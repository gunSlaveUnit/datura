from PySide6.QtCore import QObject, Signal, Property, Slot

from common.api.v1.schemas.company import CompanyCreateSchema
from desktop.src.services.CompanyService import CompanyService


class CompanyLogic(QObject):
    """
    Provides fields and functionality to provide
    the user with information about the company, payment information
    """

    juridical_name_changed = Signal()
    company_form_changed = Signal()
    street_house_apartment_changed = Signal()
    city_changed = Signal()
    region_changed = Signal()
    country_changed = Signal()
    postal_code_changed = Signal()
    notification_email_changed = Signal()
    bic_changed = Signal()
    bank_address_changed = Signal()
    bank_account_number_changed = Signal()

    drafted_new_button_state_changed = Signal()

    registered = Signal()
    notRegistered = Signal()

    def __init__(self, company_service: CompanyService):
        super().__init__()

        self._company_service: CompanyService  = company_service

        self._juridical_name = ''
        self._company_form = ''
        self._street_house_apartment = ''
        self._city = ''
        self._region = ''
        self._country = ''
        self._postal_code = ''
        self._notification_email = ''
        self._bic = ''
        self._bank_address = ''
        self._bank_account_number = ''

        self._is_drafted_new_button_enabled = False

    @Slot()
    def new(self):
        data = CompanyCreateSchema(
            juridical_name=self._juridical_name,
            form=self._company_form,
            street_house_apartment=self._street_house_apartment,
            city=self._city,
            region=self._region,
            country=self._country,
            postal_code=self._postal_code,
            notification_email=self._notification_email,
            bic=self._bic,
            bank_address=self._bank_address,
            bank_account_number=self._bank_account_number
        )

        response = self._company_service.create(data)
        if response.ok:
            self.registered.emit()

    @Slot()
    def check(self):
        self._company_service.load_personal()

        if self._company_service.company is None:
            self.notRegistered.emit()
        else:
            if self._company_service.company.is_approved:
                self.is_drafted_new_button_enabled = True
                self.drafted_new_button_state_changed.emit()
            self.registered.emit()

    juridical_name = Property(str,
                              lambda self: self._juridical_name,
                              lambda self, value: setattr(self, '_juridical_name', value),
                              notify=juridical_name_changed)
    company_form = Property(str,
                            lambda self: self._company_form,
                            lambda self, value: setattr(self, '_company_form', value),
                            notify=company_form_changed)
    street_house_apartment = Property(str,
                                      lambda self: self._street_house_apartment,
                                      lambda self, value: setattr(self, '_street_house_apartment', value),
                                      notify=street_house_apartment_changed)
    city = Property(str,
                    lambda self: self._city,
                    lambda self, value: setattr(self, '_city', value),
                    notify=city_changed)
    region = Property(str,
                      lambda self: self._region,
                      lambda self, value: setattr(self, '_region', value),
                      notify=region_changed)
    country = Property(str,
                       lambda self: self._country,
                       lambda self, value: setattr(self, '_country', value),
                       notify=country_changed)
    postal_code = Property(str,
                           lambda self: self._postal_code,
                           lambda self, value: setattr(self, '_postal_code', value),
                           notify=postal_code_changed)
    notification_email = Property(str,
                                  lambda self: self._notification_email,
                                  lambda self, value: setattr(self, '_notification_email', value),
                                  notify=notification_email_changed)
    bic = Property(str,
                   lambda self: self._bic,
                   lambda self, value: setattr(self, '_bic', value),
                   notify=bic_changed)
    bank_address = Property(str,
                            lambda self: self._bank_address,
                            lambda self, value: setattr(self, '_bank_address', value),
                            notify=bank_address_changed)
    bank_account_number = Property(str,
                                   lambda self: self._bank_account_number,
                                   lambda self, value: setattr(self, '_bank_account_number', value),
                                   notify=bank_account_number_changed)
    is_drafted_new_button_enabled = Property(bool,
                                             lambda self: self._is_drafted_new_button_enabled,
                                             lambda self, value: setattr(self, '_is_drafted_new_button_enabled', value),
                                             notify=drafted_new_button_state_changed)
