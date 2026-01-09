import { UserFormComponent } from './user-form.component';
import { customRender, screen } from '../../../../../tests/test-utils.function';
import userEvent from '@testing-library/user-event';
import { Role } from '../../../../@core/auth/models/role.enum';
import { generateUser } from '../../../../../tests/factories/user.factory';
import { User } from '../../models/user.model';

describe('UserFormComponent', () => {
  it('should have the default data', async () => {
    const { userEvent } = await setupComponent();

    const usernameInput = screen.getByLabelText(/username/i);
    expect(usernameInput).toHaveValue('');
    expect(usernameInput).toBeRequired();

    const passwordInput = screen.getByLabelText(/password/i);
    expect(passwordInput).toHaveValue('');
    expect(passwordInput).toBeRequired();

    const roleCombobox = await screen.findByRole('combobox', { name: /role/i });
    await userEvent.click(roleCombobox);
    expect(roleCombobox).toHaveTextContent(Role.Operator);
  });

  it('should have the user data on binding', async () => {
    const expectedUser = generateUser();
    const { userEvent } = await setupComponent(expectedUser);

    const usernameInput = screen.getByLabelText(/username/i);
    expect(usernameInput).toHaveValue(expectedUser.Username);

    const passwordInput = screen.getByLabelText(/password/i);
    expect(passwordInput).toHaveValue(expectedUser.Password);

    const roleCombobox = await screen.findByRole('combobox', { name: /role/i });
    await userEvent.click(roleCombobox);
    expect(roleCombobox).toHaveTextContent(expectedUser.Role);
  });

  it('should show an error when username is empty', async () => {
    const { userEvent } = await setupComponent();

    const usernameInput = screen.getByLabelText(/username/i);
    await userEvent.clear(usernameInput);
    await userEvent.tab();

    const alertElement = await screen.findByRole('alert');
    expect(alertElement).toBeInTheDocument();
    expect(alertElement).toHaveTextContent(/username/i);

    const button = await screen.findByRole('button', { name: /save/i });
    expect(button).toBeDisabled();
  });

  it.skip('should show an error when password does not follow the pattern', async () => {
    const { userEvent } = await setupComponent();

    const passwordInput = screen.getByLabelText(/password/i);
    await userEvent.type(passwordInput, 'Test1234');
    await userEvent.tab();

    expect(passwordInput).toHaveAttribute('aria-invalid', 'true');

    const alertElement = await screen.findByRole('alert');
    expect(alertElement).toHaveTextContent(/password/i);

    const button = await screen.findByRole('button', { name: /save/i });
    expect(button).toBeDisabled();
  });

  it('should emit the back event', async () => {
    const { userEvent, outputs } = await setupComponent();

    const cancelButton = await screen.findByRole('button', { name: /cancel/i });
    await userEvent.click(cancelButton);

    expect(outputs.back.emit).toHaveBeenCalledTimes(1);
    expect(outputs.save.emit).toHaveBeenCalledTimes(0);
  });

  it('should emit the save event', async () => {
    const expectedUser = generateUser();
    const { userEvent, outputs } = await setupComponent(expectedUser);

    const usernameInput = screen.getByLabelText(/username/i);
    await userEvent.clear(usernameInput);
    await userEvent.type(usernameInput, expectedUser.Username);

    const saveButton = await screen.findByRole('button', { name: /save/i });
    await userEvent.click(saveButton);

    expect(outputs.save.emit).toHaveBeenCalledTimes(1);
    expect(outputs.save.emit).toHaveBeenCalledWith(expectedUser);
  });

  async function setupComponent(user: User | null = null) {
    const event = userEvent.setup();
    const outputs = {
      save: { emit: jest.fn() },
      back: { emit: jest.fn() },
    };
    await customRender(UserFormComponent, {
      componentOutputs: outputs as any,
      componentInputs: {
        user: user,
      },
    });

    return {
      user,
      userEvent: event,
      outputs,
    };
  }
});
