import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssessmentWritingCorrectComponent } from './assessment-writing-correct.component';

describe('AssessmentWritingCorrectComponent', () => {
  let component: AssessmentWritingCorrectComponent;
  let fixture: ComponentFixture<AssessmentWritingCorrectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssessmentWritingCorrectComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssessmentWritingCorrectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
