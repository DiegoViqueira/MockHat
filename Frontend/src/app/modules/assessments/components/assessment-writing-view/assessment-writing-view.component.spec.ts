import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssessmentWritingViewComponent } from './assessment-writing-view.component';

describe('AssessmentWritingViewComponent', () => {
  let component: AssessmentWritingViewComponent;
  let fixture: ComponentFixture<AssessmentWritingViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssessmentWritingViewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssessmentWritingViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
