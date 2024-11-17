import { Component } from '@angular/core';
import { DateSelectorComponent } from "../../../components/date-selector/date-selector.component";

@Component({
  selector: 'app-staff-filter',
  standalone: true,
  imports: [DateSelectorComponent],
  templateUrl: './staff-filter.component.html',
  styleUrl: './staff-filter.component.scss'
})
export class StaffFilterComponent {

}
