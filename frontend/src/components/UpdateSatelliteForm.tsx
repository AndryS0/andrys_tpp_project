// components/UpdateSatelliteForm.tsx
import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { createData, updateData } from '../api';
import { Satellite } from '../types';

interface UpdateSatelliteFormProps {
    initialData?: Satellite;
    onClose: () => void;
}

const UpdateSatelliteForm: React.FC<UpdateSatelliteFormProps> = ({ initialData, onClose }) => {
    const queryClient = useQueryClient();

    // Local state for form inputs, using `initialData` if provided (update mode) or default values (create mode)
    const [name, setName] = useState<string>(initialData?.name || '');
    const [distanceFromPlanet, setDistanceFromPlanet] = useState<number>(initialData?.distance_from_planet || 0);
    const [planetId, setPlanetId] = useState<number>(initialData?.planet_id || 0);

    // Mutation for updating or creating a satellite
    const satelliteMutation = useMutation(
        (satellite: Partial<Satellite> & { id?: number }) =>
            initialData
                ? updateData<Satellite>('/satellite', satellite) // Update if initialData exists
                : createData<Satellite>('/satellite', satellite), // Create if initialData is undefined
        {
            onSuccess: () => {
                queryClient.invalidateQueries('satellites');
                onClose(); // Close the form after successful creation or update
            },
        }
    );

    // Form submission handler
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (initialData) {
            satelliteMutation.mutate({ id: initialData.id, name, distance_from_planet: distanceFromPlanet, planet_id: planetId });
        } else {
            satelliteMutation.mutate({ name, distance_from_planet: distanceFromPlanet, planet_id: planetId });
        }
    };

    return (
        <form onSubmit={handleSubmit} className="update-satellite-form">
            <h3>{initialData ? 'Update Satellite' : 'Create Satellite'}</h3>

            <label>
                Name:
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </label>

            <label>
                Distance from Planet (km):
                <input
                    type="number"
                    value={distanceFromPlanet}
                    onChange={(e) => setDistanceFromPlanet(parseFloat(e.target.value))}
                />
            </label>

            <label>
                Planet ID:
                <input
                    type="number"
                    value={planetId}
                    onChange={(e) => setPlanetId(parseInt(e.target.value, 10))}
                />
            </label>

            <button type="submit">{initialData ? 'Save Changes' : 'Create Satellite'}</button>
            <button type="button" onClick={onClose}>Cancel</button>
        </form>
    );
};

export default UpdateSatelliteForm;
