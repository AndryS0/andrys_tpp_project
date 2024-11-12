// types.ts
export interface Planet {
    id: number;
    name: string;
    diameter_km: number;
    star_id: number;
}

export interface Star {
    id: number;
    name: string;
    distance_ly: number;
    mass_sm: number;
}

export interface Satellite {
    id: number;
    name: string;
    distance_from_planet: number;
    planet_id: number;
}
