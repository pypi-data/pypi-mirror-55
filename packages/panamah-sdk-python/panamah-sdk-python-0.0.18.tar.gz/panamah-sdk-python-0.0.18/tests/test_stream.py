from unittest import main, mock, TestCase
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahAcesso
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestStream(TestCase):
    def test_initialization_and_operations(self):
        class ChildModel(Model):
            name = 'PRODUTO'
            schema = {
                'id': StringField(required=True)
            }

        # should not accept non-model objects on save
        stream = PanamahStream('auth', 'secret', '123')
        try:
            stream.save(None)
        except Exception as e:
            self.assertEqual(
                str(e), 'model deve ser um modelo valido do Panamah')

        # should not accept non-model objects on delete
        stream = PanamahStream('auth', 'secret', '123')
        try:
            stream.delete(None)
        except Exception as e:
            self.assertEqual(
                str(e), 'model deve ser um modelo valido do Panamah')

        # should validate models on save
        try:
            model = ChildModel()
            stream.save(model)
        except Exception as e:
            self.assertEqual(
                str(e), 'ChildModel.id -> propriedade obrigatoria')

        # should validate models on delete
        try:
            model = ChildModel()
            stream.delete(model)
        except Exception as e:
            self.assertEqual(
                str(e), 'ChildModel.id -> propriedade obrigatoria')

    def test_events(self):
        global before_save_called
        global before_delete_called

        class ChildModel(Model):
            name = 'PRODUTO'
            schema = {
                'id': StringField(required=True)
            }

        stream = PanamahStream('auth', 'secret', '123')
        before_save_called = False
        before_delete_called = False

        class TestEvents:
            def before_save(self, model, prevent_save):
                global before_save_called
                before_save_called = True
                prevent_save()

            def before_delete(self, model, prevent_delete):
                global before_delete_called
                before_delete_called = True
                prevent_delete()
                
        test_events = TestEvents()

        stream.on('before_save', test_events.before_save)
        stream.on('before_delete', test_events.before_delete)

        with mock.patch.object(stream.processor, 'save') as processor_save_method:
            processor_save_method.return_value = True
            model = ChildModel(id='1')

            stream.save(model)
            self.assertTrue(before_save_called)

            stream.delete(model)
            self.assertTrue(before_delete_called)

            before_save_called = False
            before_delete_called = False

            stream.off('before_save', test_events.before_save)
            stream.off('before_delete', test_events.before_delete)

            stream.save(model)
            stream.delete(model)

            self.assertFalse(before_save_called)
            self.assertFalse(before_delete_called)


if __name__ == '__main__':
    main()
