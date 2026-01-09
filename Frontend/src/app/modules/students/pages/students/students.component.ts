import { Component, effect, inject, OnInit, ViewChild } from '@angular/core';
import { StudentsStore } from '../../stores/students.store';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Student } from '../../models/student.model';
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import { StudentDialogComponent } from '../../components/student-dialog.component';

@Component({
  selector: 'wlk-students',
  templateUrl: './students.component.html',
  styleUrl: './students.component.scss',
  standalone: false
})
export class StudentsComponent implements OnInit {
  store = inject(StudentsStore);

  displayedColumns: string[] = ['name', 'last_name', 'email', 'status', 'edit'];
  dataSource = new MatTableDataSource<Student>([]);


  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(public dialog: MatDialog) {
    effect(() => {
      this.dataSource.data = this.store.students();
      this.dataSource.paginator = this.paginator;
    });
  }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onUpdate(element) {
    this.dialog
      .open(StudentDialogComponent, {
        data: {
          student: element,
        },
      })
      .afterClosed()
      .subscribe((x) => {
        if (x) this.store.update(x);
      });
  }
  onRegister() {
    this.dialog
      .open(StudentDialogComponent, {
        data: {
          student: undefined,
        },
      })
      .afterClosed()
      .subscribe((x) => {
        if (x) this.store.create(x);
      });
  }
}
