// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {

    uint256 favoriteNumber; 

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber: 12, name: "Boma"});

    //array of people
    People [] public people;

    //mapping string to their corresponding integer
    mapping(string=>uint256) public nameToFavouriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public  {
        people.push(People(_favoriteNumber, _name));
        nameToFavouriteNumber[_name] = _favoriteNumber;
    }

}
