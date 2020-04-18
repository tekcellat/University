#ifndef _STRUCT_H
#define _STRUCT_H

#pragma pack(push, 1)
struct excursions{
	int n_objects;
	char *excursion_type; 
};

struct beach{
	char *season;
	int t_water;
	int t_air;
	int time;
};

struct sport{
    char *sport_type;
    int min_price;	
};

struct information{
	char *country;
	int population;
	char *capital;
	char *continent;
	char *tourism_type;
	union{
		struct excursions;
		struct beach;
		struct sport;
	};
};
#pragma pack(pop)
#endif