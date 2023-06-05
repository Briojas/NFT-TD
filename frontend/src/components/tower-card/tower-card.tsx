import type React from 'react';
import { Card, Icon } from '@blueprintjs/core';
import classNames, { Value } from 'classnames';
import styles from './tower-card.module.scss';
import { useState, useEffect } from 'react';
import { BlueprintIcons_16Id } from '@blueprintjs/icons/lib/esm/generated-icons/16px/blueprint-icons-16';

export interface TowerCardProps {
    tier?: number;
    operator?: BlueprintIcons_16Id;
    priority?: number;
    data1?: Value;
    data2?: Value;
    data3?: Value;
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
    data1,
    data2,
    data3,
}: TowerCardProps) => {
    const operators = ['divide', 'cross', 'minus', 'plus', 'code'];
    const conditionals = ['Less than', 'Greater than', 'Divisible by'];
    const [isConditional, setIsConditional] = useState(false);

    var data1Name = 'Power';
    var data2Name = 'Range';
    var data3Name = 'Rate';

    if (operator === operators[2] || operator === operators[3]) {
        data2Name = 'Splash';
        data3Name = 'Radius';
    }

    useEffect(() => {
        if (operator === operators[4]) {
            setIsConditional(true);
        }
    }, [operator, operators]);

    return (
        <Card className={classNames(styles['wrapper'], className)}>
            <Card className={styles['tower']}>
                <div className={styles['card-id']}>
                    <p className={styles['tier']}>{'T' + tier}</p>
                    <div className={styles['priority-operator-selector']}>
                        {/* <button className={classNames(styles.plus, styles.adjustor)}>
                            <Icon icon="caret-up" size={6} />
                        </button>
                        <button className={styles.adjustor}>
                            <Icon icon="caret-down" size={6} />
                        </button> */}
                        <button className={styles.adjustor}>
                            <Icon icon="caret-left" size={10} />
                        </button>
                    </div>
                    <Icon icon={operator} size={14} className={styles.operator} />
                    <div className={styles['priority-operator-selector']}>
                        {/* <button className={styles.adjustor}>
                            <Icon icon="caret-up" size={6} />
                        </button>
                        <button className={styles.adjustor}>
                            <Icon icon="caret-down" size={6} />
                        </button> */}
                        <button className={styles.adjustor}>
                            <Icon icon="caret-right" size={10} />
                        </button>
                    </div>
                    <p className={styles['priority']}>{'P' + priority}</p>
                </div>
                {isConditional ? (
                    <div className={styles['card-data']}>
                        {/* <div className={styles.data}>
                            <p>{data1Name}</p>
                        </div> */}
                        <div className={styles.data}>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-left" size={6} />
                                </button>
                            </div>
                            <div className={styles['power-selector']}>
                                <p>{data1}</p>
                            </div>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-right" size={6} />
                                </button>
                            </div>
                        </div>
                        <div className={styles.data}>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-left" size={6} />
                                </button>
                            </div>
                            <div className={styles['power-selector']}>
                                <p>{data2}</p>
                            </div>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-right" size={6} />
                                </button>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className={styles['card-data']}>
                        <div className={classNames(styles.product_row, styles.data)}>
                            <p>{data1Name}</p>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-up" size={6} />
                                </button>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-down" size={6} />
                                </button>
                            </div>
                            <p className={styles['data-value']}>{data1}</p>
                        </div>
                        <div className={classNames(styles.product_row, styles.data)}>
                            <p>{data2Name}</p>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-up" size={6} />
                                </button>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-down" size={6} />
                                </button>
                            </div>
                            <p className={styles['data-value']}>{data2}</p>
                        </div>
                        <div className={styles.data}>
                            <p>{data3Name}</p>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-up" size={6} />
                                </button>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-down" size={6} />
                                </button>
                            </div>
                            <p className={styles['data-value']}>{data3}</p>
                        </div>
                    </div>
                )}
            </Card>
        </Card>
    );
};
