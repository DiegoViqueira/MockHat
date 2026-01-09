import { ToolbarComponent } from './toolbar.component';
import userEvent from '@testing-library/user-event';
import { customRender, screen } from '../../../../../tests/test-utils.function';
import { SettingsMockService } from '../../../../../tests/mocks/settings-mock.service';
import { SettingsService } from '../../../settings/services/settings.service';
import { EnvironmentMockService } from '../../../../../tests/mocks/environment-mock.service';

describe('ToolbarComponent', () => {
  it.skip('should contain the frontend version', async () => {
    const { settingsMock } = await setupComponent();

    const frontendVersion = new EnvironmentMockService().version();
    const frontendElement = screen.queryByText(frontendVersion);
    expect(frontendElement).toBeInTheDocument();

    const backendVersion = settingsMock.settings().Info.MasterVersion;
    const backendElement = await screen.findByText(backendVersion);
    expect(backendElement).toBeInTheDocument();
  });

  it('should call settings cache on component construction', async () => {
    const { settingsMock } = await setupComponent();

    expect(settingsMock.cache).toHaveBeenCalledTimes(1);
  });

  it('should open a new https://hertasecurity.com page on press link', async () => {
    await setupComponent();

    const hertaLink = screen.getByRole('link');
    expect(hertaLink).toHaveAttribute('href', 'https://hertasecurity.com');
    expect(hertaLink).toHaveAttribute('target', '_blank');
  });

  async function setupComponent() {
    const event = userEvent.setup();
    const settingsMock = new SettingsMockService();
    await customRender(ToolbarComponent, {
      providers: [{ provide: SettingsService, useValue: settingsMock }],
    });

    return {
      userEvent: event,
      settingsMock,
    };
  }
});
