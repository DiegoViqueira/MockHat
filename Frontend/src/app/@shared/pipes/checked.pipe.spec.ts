import { CheckedPipe } from './checked.pipe';

describe('CheckedPipe', () => {
  const pipe = new CheckedPipe();

  it('should transform false as cross icon', () => {
    expect(pipe.transform(false)).toEqual('close-outline');
  });

  it('should transform true as tick icon', () => {
    expect(pipe.transform(true)).toEqual('checkmark-outline');
  });
});
