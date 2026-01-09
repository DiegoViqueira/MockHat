import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassStudentsTableComponent } from './class-members-table.component';

describe('ClassStudentsTableComponent', () => {
  let component: ClassStudentsTableComponent;
  let fixture: ComponentFixture<ClassStudentsTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassStudentsTableComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ClassStudentsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
