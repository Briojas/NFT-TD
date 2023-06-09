import type React from 'react';
import { Card, Icon } from '@blueprintjs/core';
import classNames, { Value } from 'classnames';
import styles from './tower-card.module.scss';
import { useState, useEffect, useMemo, ChangeEvent } from 'react';
import { BlueprintIcons_16 } from '@blueprintjs/icons/lib/esm/generated-icons/16px/blueprint-icons-16';
import { HookCallbacks } from 'async_hooks';

export interface TowerData {
    tier: number;
    priority: number;
    operator: number;
    data1: number;
    data2: number;
    data3: number;
}

export interface TowerCardProps {
    tower: TowerData;
    update: React.Dispatch<React.SetStateAction<TowerData>>;
    children?: React.ReactNode;
    className?: string;
}

export const TowerCard = ({ className, tower, update }: TowerCardProps) => {
    const operators = [
        BlueprintIcons_16['Divide'],
        BlueprintIcons_16['Cross'],
        BlueprintIcons_16['Minus'],
        BlueprintIcons_16['Plus'],
        // BlueprintIcons_16['Code'],
    ];

    // const conditionals = [
    //     BlueprintIcons_16['LessThan'],
    //     BlueprintIcons_16['GreaterThan'],
    //     BlueprintIcons_16['Slash'],
    // ];
    // const [isConditional, setIsConditional] = useState(false);

    // Function to handle changes in the form inputs
    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        update((prevData: TowerData) => ({
            ...prevData,
            [name]: parseInt(value),
        }));
    };

    const handleOperator = (value: number) => {
        update((prevData: TowerData) => ({
            ...prevData,
            operator: value,
        }));
    };

    if (tower.operator < 0) {
        handleOperator(0);
    } else if (tower.operator > operators.length - 1) {
        handleOperator(operators.length - 1);
    }

    var data1Name = 'Power';
    var data2Name = 'Range';
    var data3Name = 'Rate';

    // if (operator === operators[2] || operator === operators[3]) {
    //     data2Name = 'Splash';
    //     data3Name = 'Radius';
    // }
    // useEffect(() => {
    //     if (operator === operators[4]) {
    //         setIsConditional(true);
    //     }
    // }, [operator, operators]);

    return (
        <Card className={classNames(styles['wrapper'], className)}>
            <Card className={styles['tower']}>
                <div className={styles['card-id']}>
                    <p className={styles['tier']}>{'T' + tower?.tier}</p>
                    <div className={styles['priority-operator-selector']}>
                        <button
                            className={styles.adjustor}
                            onClick={() => handleOperator(tower.operator - 1)}
                        >
                            <Icon icon="caret-left" size={10} />
                        </button>
                    </div>
                    <Icon icon={operators[tower.operator]} size={14} className={styles.operator} />
                    <div className={styles['priority-operator-selector']}>
                        <button
                            className={styles.adjustor}
                            onClick={() => handleOperator(tower.operator + 1)}
                        >
                            <Icon icon="caret-right" size={10} />
                        </button>
                    </div>
                    <p className={styles['priority']}>{'P' + tower?.priority}</p>
                </div>
                {/* {isConditional ? (
                    <div className={styles['card-data']}>
                        <div className={styles.data}>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-left" size={6} />
                                </button>
                            </div>
                            <div className={styles['power-selector']}>
                                <input
                                    type="number"
                                    value={data1}
                                    onChange={(e) => setData1(parseInt(e.target.value))}
                                />
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
                                <input
                                    type="number"
                                    value={data2}
                                    onChange={(e) => setData2(parseInt(e.target.value))}
                                />
                            </div>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-right" size={6} />
                                </button>
                            </div>
                        </div>
                    </div>
                ) : ( */}
                <div className={styles['card-data']}>
                    <div className={classNames(styles.product_row, styles.data)}>
                        <p>{data1Name}</p>
                        <input
                            type="number"
                            name="data1"
                            value={tower.data1}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className={classNames(styles.product_row, styles.data)}>
                        <p>{data2Name}</p>
                        <input
                            type="number"
                            name="data2"
                            value={tower.data2}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className={styles.data}>
                        <p>{data3Name}</p>
                        <input
                            type="number"
                            name="data3"
                            value={tower.data3}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={handleInputChange}
                        />
                    </div>
                </div>
            </Card>
        </Card>
    );
};
