import { Component } from '@angular/core';
import { StaffFilterComponent } from "./staff-filter/staff-filter.component";
import { StaffTableComponent } from "./staff-table/staff-table.component";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-staff-registry',
  standalone: true,
  imports: [CommonModule, StaffFilterComponent, StaffTableComponent],
  templateUrl: './staff-registry.component.html',
  styleUrl: './staff-registry.component.scss'
})
export class StaffRegistryComponent {

}
