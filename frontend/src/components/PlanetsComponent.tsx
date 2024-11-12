// components/PlanetsComponent.tsx
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchData, deleteData } from '../api';
import { Planet } from '../types';
import UpdatePlanetForm from './UpdatePlanetForm';
import './PlanetsComponent.css';

const PlanetsComponent: React.FC = () => {
    const queryClient = useQueryClient();
    const [selectedPlanet, setSelectedPlanet] = useState<Planet | null>(null); // For the planet to be updated
    const [isCreating, setIsCreating] = useState(false); // To track if the form is in create mode

    const { data: planets, isLoading } = useQuery<Planet[]>(
        'planets',
        () => fetchData<Planet[]>('/planet', { limit: 10, offset: 0 })
    );

    const deletePlanet = useMutation((id: number) => deleteData('/planet', { id }), {
        onSuccess: () => queryClient.invalidateQueries('planets'),
    });

    if (isLoading) return <p>Loading planets...</p>;

    return (
        <div className="planets-container">
            <h2>Planets</h2>
            <button onClick={() => { setIsCreating(true); setSelectedPlanet(null); }}>Create Planet</button>
            <ul>
                {planets?.map((planet) => (
                    <li key={planet.id}>
                        {planet.id}: {planet.name} - {planet.diameter_km} km
                        <button onClick={() => { setSelectedPlanet(planet); setIsCreating(false); }}>Update</button>
                        <button onClick={() => deletePlanet.mutate(planet.id)}>Delete</button>
                    </li>
                ))}
            </ul>

            {/* Render UpdatePlanetForm for creating or updating */}
            {(isCreating || selectedPlanet) && (
                <UpdatePlanetForm
                    initialData={selectedPlanet || undefined}
                    onClose={() => { setSelectedPlanet(null); setIsCreating(false); }}
                />
            )}
        </div>
    );
};

export default PlanetsComponent;
