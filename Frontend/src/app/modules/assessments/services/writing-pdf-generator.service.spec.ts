import { TestBed } from '@angular/core/testing';

import { WritingPdfGeneratorService } from './writing-pdf-generator.service';

describe('WritingPdfGeneratorService', () => {
  let service: WritingPdfGeneratorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WritingPdfGeneratorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
