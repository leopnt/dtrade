import { Component, ElementRef, OnInit } from '@angular/core';


@Component({
  selector: 'app-pheader',
  templateUrl: './pheader.component.html',
  styleUrls: ['./pheader.component.scss']
})
export class PheaderComponent implements OnInit {

  constructor(private elementRef: ElementRef) { }

  ngOnInit(): void {
    const links = document.querySelectorAll('nav a');

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const href = link.getAttribute('href');
        const target = href ? document.querySelector(href) : null;
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    document.getElementById("menuHome")?.focus()

  }



}
