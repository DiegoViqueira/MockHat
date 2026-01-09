import { YesNoPipe } from './yes-no.pipe';

describe('YesNoPipe', () => {
  const pipe = new YesNoPipe();

  it('should transform false to "no"', () => {
    expect(pipe.transform(false)).toEqual('no');
  });

  it('should transform true to "yes"', () => {
    expect(pipe.transform(true)).toEqual('yes');
  });
});
