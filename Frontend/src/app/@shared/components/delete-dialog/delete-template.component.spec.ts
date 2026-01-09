import { DeleteTemplateComponent } from './delete-template.component';
import userEvent from '@testing-library/user-event';
import { customRender, screen } from '../../../../tests/test-utils.function';
import { generateString } from '../../../../tests/factories/string.factory';

describe('DeleteTemplateComponent', () => {
  it('should title be bound', async () => {
    const { title } = await setupComponent();

    const titleElement = screen.getByText(title);

    expect(titleElement).toBeInTheDocument();
  });

  it('should emit the cancel event', async () => {
    const { output, control } = await setupComponent();

    const noButton = screen.getByRole('button', { name: /no/i });
    await control.click(noButton);

    expect(output.cancel.emit).toHaveBeenCalledTimes(1);
  });

  it('should emit the confirm event', async () => {
    const { output, control } = await setupComponent();

    const yesButton = screen.getByRole('button', { name: /yes/i });
    await control.click(yesButton);

    expect(output.confirm.emit).toHaveBeenCalledTimes(1);
  });

  async function setupComponent() {
    const title = generateString();
    const output = { cancel: { emit: jest.fn() }, confirm: { emit: jest.fn() } };
    await customRender(DeleteTemplateComponent, {
      componentInputs: {
        title: title,
      },
      componentOutputs: output as any,
    });

    return {
      output,
      title,
      control: userEvent.setup(),
    };
  }
});
