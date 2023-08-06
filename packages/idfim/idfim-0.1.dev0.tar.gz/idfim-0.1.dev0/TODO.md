# TODO

## Version 0.1

- [x] Make a first request to https://portal.api.iledefrance-mobilites.fr API (from 2 fixed points)
- [ ] Read start points from a JSON configuration file
- [x] Get isochrone map
- [ ] Write polygon result in an JSON file
- [ ] JS dataviz from saved JSON file
- [ ] Get isochrone maps at multiple hours (morning and evening) + select hour in dataviz

## Version 1.0

- [ ] Save multiples isochrone maps
- [ ] Compute intersections http://turfjs.org/docs/#intersect
- [ ] JS dataviz: select person + date / hour

## Version 1.1dev1

- [ ] Manage multiple start and end points
- [ ] Get GPS coordinates of all train / bus stations -> use them as ending points

## Version 1.1dev2

- [ ] Set interval request
- [ ] Set start / stop hours
- [ ] Compute the number of request per day (to ensure quotas are respected)

## Version 1.1dev3

- [ ] Write a systemd config file to launch idfim as a service at system startup

## Version 1.1dev4

- [ ] Write visualization / data analysis scripts
