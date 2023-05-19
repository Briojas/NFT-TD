import type React from 'react';
import { Card, Slider, Icon } from '@blueprintjs/core';
import classNames from 'classnames';
import styles from './tower-card.module.scss';
import { useState } from 'react';
import { BlueprintIcons_16Id } from '@blueprintjs/icons/lib/esm/generated-icons/16px/blueprint-icons-16';

export interface TowerCardProps {
    tier?: number;
    operator?: BlueprintIcons_16Id;
    priority?: number;
    power?: number;
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
export const TowerCard = ({ className, tier, priority, operator, power }: TowerCardProps) => {
    const [sliderValue, setSliderValue] = useState<number>(8);
    return (
        <Card className={classNames(styles['wrapper'], className)}>
            <Card className={styles['tower']}>
                <div className={styles['card-id']}>
                    <p className={styles['tier']}>{'T' + tier}</p>
                    <div>
                        <button className={classNames(styles.plus, styles.adjustor)}>
                            <Icon icon="caret-up" size={10} />
                        </button>
                        <button className={styles.adjustor}>
                            {/* <Icon icon="chevron-down" size={8} /> */}
                            <Icon icon="caret-down" size={10} />
                        </button>
                    </div>
                    <Icon icon={operator} size={20} />
                    <div>
                        <button className={styles.adjustor}>
                            <Icon icon="caret-up" size={10} />
                        </button>
                        <button className={styles.adjustor}>
                            <Icon icon="caret-down" size={10} />
                        </button>
                    </div>
                    <p className={styles['priority']}>{'P' + priority}</p>
                </div>
                <div className={classNames(styles.product_row, styles.power)}>
                    <p>Power</p>
                    <div className={styles['power-selector']}>
                        <button className={classNames(styles.plus, styles.adjustor)}>
                            <Icon icon="caret-up" size={10} />
                        </button>
                        <button className={classNames(styles.plus, styles.adjustor)}>
                            <Icon icon="caret-down" size={10} />
                        </button>
                    </div>
                    <p className={styles['data-value']}>{power}</p>
                </div>
                <div>
                    <p>Range</p>
                </div>
            </Card>
        </Card>
    );
};
