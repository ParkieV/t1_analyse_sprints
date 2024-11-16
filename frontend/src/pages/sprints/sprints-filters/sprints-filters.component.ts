import { Component } from '@angular/core';
import { DateSelectorComponent } from "../../../components/date-selector/date-selector.component";

@Component({
  selector: 'app-sprints-filters',
  standalone: true,
  imports: [DateSelectorComponent],
  templateUrl: './sprints-filters.component.html',
  styleUrl: './sprints-filters.component.scss'
})
export class SprintsFiltersComponent {

}
