import { customRender, screen } from '../../../../../tests/test-utils.function';
import userEvent from '@testing-library/user-event';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { UserFormComponent } from '../form/user-form.component';
import { UpdateUserDialogComponent } from './update-user-dialog.component';
import { HttpMock } from '../../../../../tests/mocks/http-mock.service';
import { generateUser } from '../../../../../tests/factories/user.factory';

describe('UpdateUserDialogComponent', () => {
  it('should close the dialog when close button is clicked', async () => {
    const { dialogMock, userEvent } = await setupComponent();

    const cancelButton = await screen.findByRole('button', { name: /cancel/i });
    await userEvent.click(cancelButton);

    expect(dialogMock.close).toHaveBeenCalledTimes(1);
    expect(dialogMock.close).toHaveBeenCalledWith(false);
  });

  it('should call the service update method when onSave is triggered', async () => {
    const { user, userEvent } = await setupComponent();
    // Enable save button
    const usernameInput = await screen.findByLabelText(/username/i);
    await userEvent.clear(usernameInput);
    await userEvent.type(usernameInput, user.Username);

    const saveButton = await screen.findByRole('button', { name: /save/i });
    await userEvent.click(saveButton);

    HttpMock.Request().witPathUrl('UpdateUser').expectBody({
      Id: user.Id,
      Username: user.Username,
      Password: user.Password,
      Role: user.Role,
    });
  });

  it('should call the close dialog when when the response is successful', async () => {
    const { dialogMock, user, userEvent } = await setupComponent();
    // Enable save button
    const usernameInput = await screen.findByLabelText(/username/i);
    await userEvent.clear(usernameInput);
    await userEvent.type(usernameInput, user.Username);

    const saveButton = await screen.findByRole('button', { name: /save/i });
    await userEvent.click(saveButton);

    HttpMock.Request().witPathUrl('UpdateUser').withOkResponse();

    expect(dialogMock.close).toHaveBeenCalledTimes(1); // Why two times
    expect(dialogMock.close).toHaveBeenCalledWith(true);
  });

  async function setupComponent() {
    const event = userEvent.setup();
    const user = generateUser();
    const dialogMock = {
      close: jest.fn(),
    };
    await customRender(UpdateUserDialogComponent, {
      declarations: [UserFormComponent],
      providers: [
        {
          provide: MatDialogRef<UpdateUserDialogComponent>,
          useValue: dialogMock,
        },
        {
          provide: MAT_DIALOG_DATA,
          useValue: user,
        },
      ],
    });

    return {
      dialogMock,
      user,
      userEvent: event,
    };
  }
});
