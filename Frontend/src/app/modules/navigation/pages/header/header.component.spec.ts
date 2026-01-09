import { HeaderComponent } from './header.component';
import userEvent from '@testing-library/user-event';
import { customRender } from '../../../../../tests/test-utils.function';
import { EventMqttMockService } from '../../../../../tests/mocks/event-mqtt-mock.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { LocalStorageService } from '../../../../@core/auth/services/local-storage.service';
import { generateUserSystem } from '../../../../../tests/factories/user-system.factory';
import { screen, waitFor } from '@testing-library/angular';
import { EventMqttService } from '../../../../@core/services/event.mqtt.service';
import { MasterHealthService } from '../../../../@core/services/master-health.service';
import { MasterHealthMockService } from '../../../../../tests/mocks/master-health-mock.service';
import { HttpMock } from '../../../../../tests/mocks/http-mock.service';
import { Router } from '@angular/router';

describe('HeaderComponent', () => {
  it('should display the user name', async () => {
    const user = generateUserSystem();
    new LocalStorageService().set('user', user);

    await setupComponent();

    const usernameText = screen.getByText(user.username);
    expect(usernameText).toBeInTheDocument();

    const usernameButton = screen.getByLabelText(/username/i);
    expect(usernameButton).toBeInTheDocument();
  });

  it('should call logout http request', async () => {
    const user = generateUserSystem();
    const storage = new LocalStorageService();
    storage.set('user', user);

    const { userEvent } = await setupComponent();

    const usernameButton = screen.getByLabelText(/username/i);
    await userEvent.click(usernameButton);

    const logoutButton = await screen.findByRole('menuitem', { name: /logout/i });
    await userEvent.click(logoutButton);

    HttpMock.Request().witPathUrl('LogOut').expectBody();
  });

  it('should clean user data on logout', async () => {
    const user = generateUserSystem();
    const storage = new LocalStorageService();
    storage.set('user', user);

    const { router, userEvent } = await setupComponent();

    const usernameButton = screen.getByLabelText(/username/i);
    await userEvent.click(usernameButton);

    const logoutButton = await screen.findByRole('menuitem', { name: /logout/i });
    await userEvent.click(logoutButton);

    HttpMock.Request().witPathUrl('LogOut').withOkResponse();

    await waitFor(() => {
      expect(storage.get('user')).toBeNull();
      expect(storage.get('token')).toBeNull();
    });

    expect(router.navigateByUrl).toHaveBeenCalledTimes(1);
    expect(router.navigateByUrl).toHaveBeenCalledWith('auth/login');
  });

  it('should go to profile on press profile button', async () => {
    const user = generateUserSystem();
    const storage = new LocalStorageService();
    storage.set('user', user);

    const { router, userEvent } = await setupComponent();

    const usernameButton = screen.getByLabelText(/username/i);
    await userEvent.click(usernameButton);

    const logoutButton = await screen.findByRole('menuitem', { name: /profile/i });
    await userEvent.click(logoutButton);

    expect(router.navigateByUrl).toHaveBeenCalledTimes(1);
    expect(router.navigateByUrl).toHaveBeenCalledWith('modules/profile');
  });

  it('should broker display as warning when it is failing', async () => {
    const { mqtt } = await setupComponent();
    mqtt.statusResponse.set(false);

    await waitFor(() => {
      const brokerButton = screen.getByLabelText(/broker/i);
      expect(brokerButton).toHaveAttribute('ng-reflect-color', 'warn');
    });
  });

  it('should broker display as primary when it is working', async () => {
    const { mqtt } = await setupComponent();
    mqtt.statusResponse.set(true);

    await waitFor(() => {
      const brokerButton = screen.getByLabelText(/broker/i);
      expect(brokerButton).toHaveAttribute('ng-reflect-color', 'primary');
    });
  });

  it('should Master display as warning when it is failing', async () => {
    const { health } = await setupComponent();
    health.statusResponse.set(false);

    await waitFor(() => {
      const brokerButton = screen.getByLabelText(/master/i);
      expect(brokerButton).toHaveAttribute('ng-reflect-color', 'warn');
    });
  });

  it('should Master display as primary when it is working', async () => {
    const { health } = await setupComponent();
    health.statusResponse.set(true);

    await waitFor(() => {
      const brokerButton = screen.getByLabelText(/master/i);
      expect(brokerButton).toHaveAttribute('ng-reflect-color', 'primary');
    });
  });

  async function setupComponent() {
    const event = userEvent.setup();
    const health = new MasterHealthMockService();
    const mqtt = new EventMqttMockService();
    const router = {
      navigateByUrl: jest.fn(),
    };
    await customRender(HeaderComponent, {
      providers: [
        { provide: JwtHelperService, useValue: new JwtHelperService() },
        { provide: EventMqttService, useValue: mqtt },
        { provide: MasterHealthService, useValue: health },
        { provide: Router, useValue: router },
      ],
    });

    return {
      health,
      mqtt,
      router,
      userEvent: event,
    };
  }
});
