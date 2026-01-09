import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssessmentWritingDetailsComponent } from './assessment-writing-details.component';

describe('AssessmentWritingDetailsComponent', () => {
  let component: AssessmentWritingDetailsComponent;
  let fixture: ComponentFixture<AssessmentWritingDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssessmentWritingDetailsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssessmentWritingDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
