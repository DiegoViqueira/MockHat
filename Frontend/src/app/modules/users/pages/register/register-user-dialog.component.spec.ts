import { RegisterUserDialogComponent } from './register-user-dialog.component';
import { customRender, screen } from '../../../../../tests/test-utils.function';
import userEvent from '@testing-library/user-event';
import { MatDialogRef } from '@angular/material/dialog';
import { UserFormComponent } from '../form/user-form.component';
import { HttpMock } from '../../../../../tests/mocks/http-mock.service';
import { generateUser } from '../../../../../tests/factories/user.factory';
import { UpdateUserDialogComponent } from '../update/update-user-dialog.component';

describe('RegisterUserDialogComponent', () => {
  it('should close the dialog when close button is clicked', async () => {
    const { dialogMock, userEvent } = await setupComponent();

    const cancelButton = await screen.findByRole('button', { name: /cancel/i });
    await userEvent.click(cancelButton);

    expect(dialogMock.close).toHaveBeenCalledTimes(1);
    expect(dialogMock.close).toHaveBeenCalledWith(false);
  });

  it('should call the service registration method when onSave is triggered', async () => {
    const user = generateUser();
    const { userEvent } = await setupComponent();

    const usernameInput = screen.getByLabelText(/username/i);
    await userEvent.type(usernameInput, user.Username);

    const passwordInput = screen.getByLabelText(/password/i);
    await userEvent.type(passwordInput, user.Password);

    const roleComboBox = screen.getByRole('combobox');
    await userEvent.click(roleComboBox);
    const selectedOption = screen.getByRole('option', { name: user.Role });
    await userEvent.click(selectedOption);

    const button = await screen.findByRole('button', { name: /save/i });
    await userEvent.click(button);

    HttpMock.Request().witPathUrl('RegisterUser').withOkResponse().expectBody({
      Username: user.Username,
      Password: user.Password,
      Role: user.Role,
    });
  });

  it('should call the close dialog when response is successful', async () => {
    const user = generateUser();
    const { dialogMock, userEvent } = await setupComponent();

    const usernameInput = await screen.findByLabelText(/username/i);
    await userEvent.type(usernameInput, user.Username);

    const passwordInput = await screen.findByLabelText(/password/i);
    await userEvent.type(passwordInput, user.Password);

    const roleComboBox = await screen.findByRole('combobox');
    await userEvent.click(roleComboBox);
    const selectedOption = await screen.findByRole('option', { name: user.Role });
    await userEvent.click(selectedOption);

    const saveButton = await screen.findByRole('button', { name: /save/i });
    await userEvent.click(saveButton);

    HttpMock.Request().witPathUrl('RegisterUser').withOkResponse();

    expect(dialogMock.close).toHaveBeenCalledTimes(1);
    expect(dialogMock.close).toHaveBeenCalledWith(true);
  });

  async function setupComponent() {
    const event = userEvent.setup();
    const dialogMock = {
      close: jest.fn(),
    };

    await customRender(RegisterUserDialogComponent, {
      providers: [{ provide: MatDialogRef<UpdateUserDialogComponent>, useValue: dialogMock }],
      declarations: [UserFormComponent],
    });
    return {
      dialogMock,
      userEvent: event,
    };
  }
});
