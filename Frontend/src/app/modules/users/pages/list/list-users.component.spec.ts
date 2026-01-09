import userEvent from '@testing-library/user-event';
import { customRender, screen } from '../../../../../tests/test-utils.function';
import { UserFormComponent } from '../form/user-form.component';
import { ListUsersComponent } from './list-users.component';
import { RegisterUserDialogComponent } from '../register/register-user-dialog.component';
import { UpdateUserDialogComponent } from '../update/update-user-dialog.component';
import { HttpMock } from '../../../../../tests/mocks/http-mock.service';
import { of } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { generateUser } from '../../../../../tests/factories/user.factory';
import { DeleteUserDialogComponent } from '../delete/delete-user-dialog.component';
import { dialogConfigFactory } from '../../../../@shared/common-environment/common-environment';
import { DatePipe } from '@angular/common';
import { YesNoPipe } from '../../../../@shared/pipes/yes-no.pipe';

describe('ListUsersComponent', () => {
  it('should show a user in the table', async () => {
    await setupComponent();

    const user = generateUser();
    HttpMock.Request().witPathUrl('ListUsers').withOkResponse([user]);

    await screen.findByText(user.Username);

    const table = screen.getAllByRole('rowgroup');
    const rows = table[1].children;
    expect(rows.length).toEqual(1);

    const row = rows[0];
    const cells = row.querySelectorAll('td');
    expect(cells.length).toEqual(5);

    expect(cells[0]).toContainHTML(user.Username);
    expect(cells[1]).toContainHTML(user.Role);
    expect(cells[2]).toContainHTML(new YesNoPipe().transform(user.IsBlocked));
    expect(cells[3]).toContainHTML(new DatePipe('en').transform(user.CreatedAt, 'short'));
  });

  it('should open a register dialog', async () => {
    const { userEvent, dialog } = await setupComponent();

    const expectedConfig = dialogConfigFactory({ width: '30%' });
    const registerButton = screen.getByRole('button', { name: /register/i });
    await userEvent.click(registerButton);

    expect(dialog.open).toHaveBeenCalledTimes(1);
    expect(dialog.open).toHaveBeenCalledWith(RegisterUserDialogComponent, expectedConfig);
  });

  it('should open the update dialog with the correct data', async () => {
    const { userEvent, dialog } = await setupComponent();

    const user = generateUser();
    const expectedConfig = dialogConfigFactory({ data: user, width: '30%' });

    HttpMock.Request().witPathUrl('ListUsers').withOkResponse([user]);

    const actionsButton = await screen.findByRole('button', {
      name: /actions/i,
    });
    await userEvent.click(actionsButton);

    const editButton = await screen.findByRole('menuitem', { name: /edit/i });
    await userEvent.click(editButton);

    expect(dialog.open).toHaveBeenCalledTimes(1);
    expect(dialog.open).toHaveBeenCalledWith(UpdateUserDialogComponent, expectedConfig);
  });

  it('should open the delete dialog with the correct data', async () => {
    const { userEvent, dialog } = await setupComponent();

    const user = generateUser();
    const expectedConfig = dialogConfigFactory({ data: user, width: '30%' });
    HttpMock.Request().witPathUrl('ListUsers').withOkResponse([user]);

    const actionsButton = await screen.findByRole('button', {
      name: /actions/i,
    });
    await userEvent.click(actionsButton);

    const deleteButton = await screen.findByRole('menuitem', { name: /delete/i });
    await userEvent.click(deleteButton);

    expect(dialog.open).toHaveBeenCalledTimes(1);
    expect(dialog.open).toHaveBeenCalledWith(DeleteUserDialogComponent, expectedConfig);
  });

  async function setupComponent() {
    const event = userEvent.setup();
    const dialog = {
      open: jest.fn(() => ({
        afterClosed: () => of(true),
      })),
    };
    await customRender(ListUsersComponent, {
      declarations: [
        RegisterUserDialogComponent,
        UpdateUserDialogComponent,
        DeleteUserDialogComponent,
        UserFormComponent,
      ],
      providers: [{ provide: MatDialog, useValue: dialog }],
    });

    return {
      dialog,
      userEvent: event,
    };
  }
});
