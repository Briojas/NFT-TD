import { createBoard } from '@wixc3/react-board';
import { TowerCard } from '../../../components/tower-card/tower-card';

const itemPhoto =
    'https://static.wixstatic.com/media/610b66_58b938ac4bc14e5a8c19a65b57d2162a~mv2.png'; // macchiato.png (530x620)

export default createBoard({
    name: 'Esspresso Macchiato',
    Board: () => (
        <TowerCard
            itemDescription="A European-style classic. Rich espresso marked with dollop of steamed milk and foam."
            itemName="Espresso Macchiato"
            itemPhotoURL={itemPhoto}
            itemPrice={9.5}
        />
    ),
    environmentProps: {
        windowWidth: 1920,
        windowHeight: 1080,
    },
});
