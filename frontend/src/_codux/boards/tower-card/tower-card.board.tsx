import { createBoard } from '@wixc3/react-board';
import { TowerCard } from '../../../components/tower-card/tower-card';

const tower = {
    tier: 3,
    priority: 2,
    operator: 3,
    data1: 2,
    data2: 11,
    data3: 9,
};

export default createBoard({
    name: 'TowerCard',
    Board: () => <TowerCard tower={tower} />,
    environmentProps: {
        windowWidth: 375,
        windowHeight: 667,
        canvasWidth: 298,
    },
});
