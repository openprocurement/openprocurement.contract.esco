# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    json_view,
    upload_file,
    context_unpack,
    update_file_content_type,
)
from openprocurement.api.validation import (
    validate_file_update,
    validate_file_upload,
    validate_patch_document_data,
)
from openprocurement.contracting.api.utils import (
    save_contract,
    contractingresource,
)
from openprocurement.contracting.core.utils import (
    apply_patch,
)
from openprocurement.contracting.core.validation import (
    validate_add_document_to_active_change,
    validate_contract_document_operation_not_in_allowed_contract_status,
)
from openprocurement.contracting.common.views.document import (
    ContractsDocumentResource as BaseContractsDocumentResource,
)
from openprocurement.contracting.esco.validation import (
    validate_scheduled_milestone_document_operation,
    validate_terminated_milestone_document_operation,
)


@contractingresource(
    name='esco:Contract Documents',
    collection_path='/contracts/{contract_id}/documents',
    path='/contracts/{contract_id}/documents/{document_id}',
    contractType='esco',
    description="Contract related binary files (PDFs, etc.)"
)
class ContractsDocumentResource(BaseContractsDocumentResource):
    """ ESCO Contract documents resource """

    @json_view(permission='upload_contract_documents',
               validators=(validate_file_upload,
                           validate_contract_document_operation_not_in_allowed_contract_status,
                           validate_scheduled_milestone_document_operation,
                           validate_terminated_milestone_document_operation,))
    def collection_post(self):
        """Contract Document Upload"""
        document = upload_file(self.request)
        self.context.documents.append(document)
        if save_contract(self.request):
            self.LOGGER.info('Created contract document {}'.format(document.id),
                             extra=context_unpack(
                                self.request, {'MESSAGE_ID': 'contract_document_create'}, {'document_id': document.id}))
            self.request.response.status = 201
            document_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=document_route, document_id=document.id, _query={})
            return {'data': document.serialize("view")}

    @json_view(permission='upload_contract_documents',
               validators=(validate_file_update,
                           validate_contract_document_operation_not_in_allowed_contract_status,
                           validate_scheduled_milestone_document_operation,
                           validate_terminated_milestone_document_operation,))
    def put(self):
        """Contract Document Update"""
        document = upload_file(self.request)
        self.request.validated['contract'].documents.append(document)
        if save_contract(self.request):
            self.LOGGER.info('Updated contract document {}'.format(self.request.context.id),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'contract_document_put'}))
            return {'data': document.serialize("view")}



    @json_view(content_type="application/json", permission='upload_contract_documents',
               validators=(validate_patch_document_data,
                           validate_contract_document_operation_not_in_allowed_contract_status,
                           validate_add_document_to_active_change,
                           validate_scheduled_milestone_document_operation,
                           validate_terminated_milestone_document_operation,))
    def patch(self):
        """Contract Document Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            self.LOGGER.info('Updated contract document {}'.format(self.request.context.id),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'contract_document_patch'}))
            return {'data': self.request.context.serialize("view")}
