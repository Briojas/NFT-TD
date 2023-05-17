import { createBoard } from '@wixc3/react-board';
import { TowerCard } from '../../../components/tower-card/tower-card';

export default createBoard({
    name: 'TowerCard',
    Board: () => <TowerCard tier={1} operator="*" priority={5} />,
    environmentProps: {
        windowWidth: 375,
        windowHeight: 667,
        canvasWidth: 298,
    },
});
