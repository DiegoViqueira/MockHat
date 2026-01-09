import { customRender, screen } from '../../../../../tests/test-utils.function';
import userEvent from '@testing-library/user-event';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpMock } from '../../../../../tests/mocks/http-mock.service';
import { generateUser } from '../../../../../tests/factories/user.factory';
import { DeleteUserDialogComponent } from './delete-user-dialog.component';
import { User } from '../../models/user.model';

describe('DeleteUserDialogComponent', () => {
  it('should close the dialog when close button is clicked', async () => {
    const { userEvent, dialogMock } = await setupComponent();

    const noButton = await screen.findByRole('button', { name: /no/i });
    await userEvent.click(noButton);

    expect(dialogMock.close).toHaveBeenCalledTimes(1);
    expect(dialogMock.close).toHaveBeenCalledWith(false);
  });

  it('should call the service delete method when onConfirm is triggered', async () => {
    const { userEvent, user } = await setupComponent();

    const yesButton = await screen.findByRole('button', { name: /yes/i });
    await userEvent.click(yesButton);

    HttpMock.Request().witPathUrl('DeleteUser').expectBody({
      Id: user.Id,
    });
  });

  it('should call the close dialog when when the response is successful', async () => {
    const { userEvent, dialogMock } = await setupComponent();

    const yesButton = await screen.findByRole('button', { name: /yes/i });
    await userEvent.click(yesButton);

    HttpMock.Request().witPathUrl('DeleteUser').withOkResponse();

    expect(dialogMock.close).toHaveBeenCalledTimes(1);
    expect(dialogMock.close).toHaveBeenCalledWith(true);
  });

  async function setupComponent(user: User = generateUser()) {
    const event = userEvent.setup();
    const dialogMock = {
      close: jest.fn(),
    };
    await customRender(DeleteUserDialogComponent, {
      providers: [
        {
          provide: MatDialogRef<DeleteUserDialogComponent>,
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
