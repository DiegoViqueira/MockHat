import { Base64ImagePipe } from './base64-image.pipe';
import { generateImage } from '../../../tests/factories/file.factory';

it('should transform false as cross icon', () => {
  const sut = new Base64ImagePipe();
  const image = generateImage();

  const response = sut.transform(image.Image);

  expect(response).toEqual(`data:image/png;base64,${image.Image}`);
});
