import { Component } from '@angular/core';
import { DateSelectorComponent } from "../../../components/date-selector/date-selector.component";

@Component({
  selector: 'app-home-filters',
  standalone: true,
  imports: [DateSelectorComponent],
  templateUrl: './home-filters.component.html',
  styleUrl: './home-filters.component.scss'
})
export class HomeFiltersComponent {

}
