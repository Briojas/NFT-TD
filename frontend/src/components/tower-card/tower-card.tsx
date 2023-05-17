import type React from 'react';
import { Elevation, Card } from '@blueprintjs/core';
import classNames from 'classnames';
import styles from './tower-card.module.scss';

export interface TowerCardProps {
    tier?: number;
    operator?: string;
    priority?: number;
    isFavorite?: boolean;
    children?: React.ReactNode;
    className?: string;
}

/**
 * This Product Item component is a simple demo component to showcase the capabilities of Codux,
 * it is a basic implementation, which is not meant to be utilized in a production environment.
 *
 * Use this demo to get a feel for how easy and fun it is to create and edit components in Codux using Blueprint.js, a 3rd party React-based UI toolkit.
 *
 */
export const TowerCard = ({
    className,
    tier,
    priority,
    operator,
    isFavorite = false,
    children,
}: TowerCardProps) => {
    return (
        <Card className={classNames(styles['wrapper'], className)} elevation={Elevation.FOUR}>
            <Card className={styles['tower']}>
                <div className={styles['card-id']}>
                    <p className={styles['tier']}>{'T' + tier}</p>
                    <p className={styles['operator']}>{operator}</p>
                    <p className={styles['priority']}>{'P' + priority}</p>
                </div>
                <div className={styles.product_row}>
                    <p className={styles.product_option}>Big</p>
                    <input type="radio" name="radio" defaultChecked />
                </div>
                <div className={styles.product_row}>
                    <p className={styles.product_option}>Medium</p>
                    <input type="radio" name="radio" />
                </div>
                <div className={styles.product_row}>
                    <p className={styles.product_option}>Small</p>
                    <input type="radio" name="radio" />
                </div>
            </Card>
        </Card>
    );
};
