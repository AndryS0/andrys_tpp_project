// components/SatellitesComponent.tsx
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchData, deleteData } from '../api';
import { Satellite } from '../types';
import UpdateSatelliteForm from './UpdateSatelliteForm';
import './SatellitesComponent.css';

const SatellitesComponent: React.FC = () => {
    const queryClient = useQueryClient();
    const [selectedSatellite, setSelectedSatellite] = useState<Satellite | null>(null); // For the satellite to be updated
    const [isCreating, setIsCreating] = useState(false); // To track if the form is in create mode

    const { data: satellites, isLoading } = useQuery<Satellite[]>(
        'satellites',
        () => fetchData<Satellite[]>('/satellite', { limit: 10, offset: 0 })
    );

    const deleteSatellite = useMutation((id: number) => deleteData('/satellite', { id }), {
        onSuccess: () => queryClient.invalidateQueries('satellites'),
    });

    if (isLoading) return <p>Loading satellites...</p>;

    return (
        <div className="satellites-container">
            <h2>Satellites</h2>
            <button onClick={() => { setIsCreating(true); setSelectedSatellite(null); }}>Create Satellite</button>
            <ul>
                {satellites?.map((satellite) => (
                    <li key={satellite.id}>
                        {satellite.id}: {satellite.name} - {satellite.distance_from_planet} km
                        <button onClick={() => { setSelectedSatellite(satellite); setIsCreating(false); }}>Update</button>
                        <button onClick={() => deleteSatellite.mutate(satellite.id)}>Delete</button>
                    </li>
                ))}
            </ul>

            {/* Render UpdateSatelliteForm for creating or updating */}
            {(isCreating || selectedSatellite) && (
                <UpdateSatelliteForm
                    initialData={selectedSatellite || undefined}
                    onClose={() => { setSelectedSatellite(null); setIsCreating(false); }}
                />
            )}
        </div>
    );
};

export default SatellitesComponent;
